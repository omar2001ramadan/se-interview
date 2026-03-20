from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import numpy as np
from openai import OpenAI
from phoenix.client import Client

from travel_assistant.schemas import (
    ArchitectureContent,
    BoundaryEmbeddingResponse,
    BoundaryProjectionRequest,
    BoundaryProjectionResponse,
    BoundaryEmbeddingSummary,
    BoundaryEmbeddingPoint,
    BoundaryMatrixCell,
    BoundaryMatrixRow,
    CorpusDescriptor,
    CorpusManifest,
    DemoOverview,
    EvaluationResult,
    EvaluationResultsResponse,
    EvaluationSummary,
    FrustratedInteraction,
    FrustratedInteractionsResponse,
    SpanSummary,
    TraceDetail,
    TraceListItem,
    TraceListResponse,
)
from travel_assistant.query_loader import session_id_for_prompt

TOOL_NAMES = {"search_attractions", "search_web"}
BACKEND_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = BACKEND_ROOT / "artifacts"
EVALS_DIR = BACKEND_ROOT / "evals"
PRESENTATION_ROOT = BACKEND_ROOT.parent / "presentation"
MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*(.*?)```", re.DOTALL)
REFUSAL_PATTERNS = (
    "can't book",
    "cannot book",
    "can't reserve",
    "cannot reserve",
    "can't purchase",
    "cannot purchase",
    "can't complete the booking",
    "cannot complete the booking",
    "i can't make reservations",
    "i cannot make reservations",
)
BOOKING_KEYWORDS = ("book", "booking", "reserve", "reservation", "ticket", "tickets", "hotel", "flight")
REDIRECT_PATTERNS = ("help you", "plan", "recommend", "find", "guide", "suggest")


def _rows_from_dataframe(dataframe: Any, *, index_label: str = "span_id") -> list[dict[str, Any]]:
    if hasattr(dataframe, "reset_index"):
        index_name = getattr(dataframe.index, "name", None)
        if index_name and index_name in dataframe.columns:
            normalized = dataframe.reset_index(drop=True)
        else:
            normalized = dataframe.reset_index()
            if "index" in normalized.columns and index_label not in normalized.columns:
                normalized = normalized.rename(columns={"index": index_label})
        return list(normalized.to_dict(orient="records"))
    if isinstance(dataframe, list):
        return list(dataframe)
    return list(dataframe or [])


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return path.read_text()
    except Exception:
        return None


def _truncate(value: Any, *, limit: int = 220) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = re.sub(r"\s+", " ", text)
    if len(text) <= limit:
        return text
    return f"{text[: limit - 1].rstrip()}…"


def _parse_datetime(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _format_datetime(value: Any) -> str | None:
    parsed = _parse_datetime(value)
    return parsed.isoformat() if parsed else (_truncate(value, limit=48) if value else None)


def _duration_ms(start_time: Any, end_time: Any) -> float | None:
    start = _parse_datetime(start_time)
    end = _parse_datetime(end_time)
    if not start or not end:
        return None
    return round((end - start).total_seconds() * 1000, 2)


def _phoenix_trace_url(base_url: str | None, project_name: str | None, trace_id: str) -> str | None:
    if not base_url:
        return None
    if not project_name:
        return base_url
    return f"{base_url.rstrip('/')}/projects/{project_name}/traces/{trace_id}"


def _prompt_from_row(row: dict[str, Any]) -> str | None:
    input_messages = row.get("attributes.llm.input_messages")
    if isinstance(input_messages, list):
        for message in input_messages:
            if isinstance(message, dict) and message.get("message.role") == "user":
                return _truncate(message.get("message.content"))
    metadata = row.get("attributes.metadata")
    if isinstance(metadata, dict):
        prompt = metadata.get("prompt")
        if prompt:
            return _truncate(prompt)
    return _truncate(row.get("attributes.input.value"))


def _session_id_from_row(row: dict[str, Any]) -> str | None:
    session_id = row.get("attributes.session.id")
    return str(session_id) if session_id else None


def _tool_names_from_rows(rows: list[dict[str, Any]]) -> list[str]:
    observed: list[str] = []
    for row in rows:
        name = str(row.get("name", "")).strip()
        if name in TOOL_NAMES and name not in observed:
            observed.append(name)
    return observed


def _llm_span_count(rows: list[dict[str, Any]]) -> int:
    count = 0
    for row in rows:
        kind = str(row.get("attributes.openinference.span.kind") or row.get("span_kind") or "").upper()
        if kind == "LLM":
            count += 1
    return count


def _error_message(row: dict[str, Any]) -> str | None:
    events = row.get("events")
    if isinstance(events, list):
        for event in events:
            if not isinstance(event, dict):
                continue
            attributes = event.get("attributes")
            if isinstance(attributes, dict) and attributes.get("exception.message"):
                return _truncate(attributes.get("exception.message"), limit=260)
    status_message = row.get("status_message")
    if status_message:
        return _truncate(status_message, limit=260)
    return None


def _input_preview(row: dict[str, Any]) -> str | None:
    return (
        _truncate(row.get("attributes.input.value"))
        or _truncate(row.get("attributes.input.mime_type"))
        or _prompt_from_row(row)
    )


def _output_preview(row: dict[str, Any]) -> str | None:
    return _truncate(row.get("attributes.output.value"))


def _load_markdown_bullets(document: str) -> list[str]:
    bullets: list[str] = []
    for line in document.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def _expected_refusal(prompt: str) -> bool:
    lowered = prompt.lower()
    return any(keyword in lowered for keyword in BOOKING_KEYWORDS)


def _actual_refusal(response_text: str, notes: list[str]) -> bool:
    lowered = response_text.lower()
    return any(pattern in lowered for pattern in REFUSAL_PATTERNS) or "planning_only" in notes


def _confusion_label(*, expected_refusal: bool, actual_refusal: bool) -> str:
    if expected_refusal and actual_refusal:
        return "tp"
    if expected_refusal and not actual_refusal:
        return "fn"
    if not expected_refusal and actual_refusal:
        return "fp"
    return "tn"


def _success_from_confusion_label(confusion_label: str, *, response_text: str, notes: list[str]) -> tuple[str, float]:
    if confusion_label in {"fp", "fn"}:
        return "fails", 0.0
    if confusion_label == "tp":
        lowered = response_text.lower()
        helpful_redirect = any(pattern in lowered for pattern in REDIRECT_PATTERNS)
        if helpful_redirect:
            return "works", 1.0
        return "partial", 0.5
    return "works", 1.0


class DemoDataService:
    def __init__(self, settings, *, client_factory: Callable[[], Client] | None = None):
        self.settings = settings
        self._client_factory = client_factory or (lambda: Client(base_url=self.settings.phoenix_base_url))
        self._embedding_payload_cache: dict[str, dict[str, Any]] = {}

    def _client(self) -> Client:
        return self._client_factory()

    def _load_artifact_rows(self, name: str, *, default: Any) -> Any:
        return _read_json(ARTIFACTS_DIR / name, default)

    def _load_corpus_rows(self, name: str, *, default: Any) -> Any:
        return _read_json(EVALS_DIR / name, default)

    def _embedding_client(self) -> OpenAI | None:
        if not self.settings.openai_api_key:
            return None
        return OpenAI(api_key=self.settings.openai_api_key)

    def _embed_texts(self, texts: list[str], *, model: str = "text-embedding-3-small") -> list[list[float]]:
        client = self._embedding_client()
        if client is None:
            raise RuntimeError("OPENAI_API_KEY is required to calculate embedding spaces.")
        response = client.embeddings.create(model=model, input=texts)
        return [list(item.embedding) for item in response.data]

    def _project_embeddings(self, embeddings: list[list[float]]) -> tuple[np.ndarray, list[float], list[list[float]]]:
        matrix = np.asarray(embeddings, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] == 0:
            raise RuntimeError("Embedding matrix is empty.")
        mean_vector = matrix.mean(axis=0)
        centered = matrix - mean_vector
        _, _, vt = np.linalg.svd(centered, full_matrices=False)
        component_count = min(3, vt.shape[0])
        components = vt[:component_count]
        if component_count < 3:
            padding = np.zeros((3 - component_count, matrix.shape[1]), dtype=float)
            components = np.vstack([components, padding])
        projected = centered @ components.T
        max_abs = float(np.max(np.abs(projected))) or 1e-9
        normalized = projected / max_abs
        return normalized, mean_vector.tolist(), components.tolist()

    def _build_embedding_payload(
        self,
        *,
        corpus_id: str,
        dataset_name: str,
        prompts: list[str],
        points: list[dict[str, Any]],
        embedding_model: str = "text-embedding-3-small",
        generated_at: str | None = None,
    ) -> dict[str, Any]:
        embeddings = self._embed_texts(prompts, model=embedding_model)
        projected, mean_vector, components = self._project_embeddings(embeddings)
        normalized_points: list[dict[str, Any]] = []
        for index, point in enumerate(points):
            normalized_points.append(
                {
                    **point,
                    "corpus_id": corpus_id,
                    "coords": {
                        "x": round(float(projected[index][0]), 4),
                        "y": round(float(projected[index][1]), 4),
                        "z": round(float(projected[index][2]), 4),
                    },
                }
            )

        worked = sum(1 for point in normalized_points if point.get("success_label") == "works")
        partial = sum(1 for point in normalized_points if point.get("success_label") == "partial")
        failed = sum(1 for point in normalized_points if point.get("success_label") == "fails")

        category_vectors: dict[str, list[np.ndarray]] = defaultdict(list)
        for point, embedding in zip(normalized_points, embeddings, strict=False):
            category_vectors[str(point.get("category") or "unknown")].append(np.asarray(embedding, dtype=float))

        matrix_rows: list[dict[str, Any]] = []
        category_names = sorted(category_vectors.keys())
        centroids = {
            category: np.mean(vectors, axis=0)
            for category, vectors in category_vectors.items()
            if vectors
        }
        for row_name in category_names:
            row_values: list[dict[str, Any]] = []
            row_centroid = centroids[row_name]
            row_norm = float(np.linalg.norm(row_centroid)) or 1e-9
            for column_name in category_names:
                column_centroid = centroids[column_name]
                column_norm = float(np.linalg.norm(column_centroid)) or 1e-9
                similarity = float(np.dot(row_centroid, column_centroid) / (row_norm * column_norm))
                row_values.append({"column": column_name, "similarity": round(similarity, 4)})
            matrix_rows.append({"row": row_name, "values": row_values})

        return {
            "generated_at": generated_at or datetime.now().astimezone().isoformat(),
            "dataset_name": dataset_name,
            "embedding_model": embedding_model,
            "dimensions": 3,
            "summary": {
                "total_prompts": len(normalized_points),
                "worked": worked,
                "partial": partial,
                "failed": failed,
                "success_rate": round((worked + 0.5 * partial) / max(len(normalized_points), 1), 4),
            },
            "points": normalized_points,
            "category_similarity_matrix": matrix_rows,
            "projection_basis": {
                "mean": mean_vector,
                "components": components,
            },
        }

    def _boundary_embedding_payload(self) -> dict[str, Any]:
        payload = self._load_artifact_rows("boundary_embedding_space.json", default={})
        if not payload:
            return {}
        points = []
        for row in payload.get("points", []):
            if not isinstance(row, dict):
                continue
            points.append({**row, "corpus_id": "boundary"})
        return {**payload, "points": points}

    def _evaluation_embedding_payload(self) -> dict[str, Any]:
        if "evaluation" in self._embedding_payload_cache:
            return self._embedding_payload_cache["evaluation"]

        query_runs = self._load_artifact_rows("query_runs.json", default=[])
        tool_rows, frustration_rows = self._load_artifact_rows("tool_usage_evaluations.json", default=[]), self._load_artifact_rows(
            "user_frustration_evaluations.json", default=[]
        )
        if not query_runs:
            return {}

        tool_by_session = {
            str(row.get("session_id")): row
            for row in tool_rows
            if isinstance(row, dict) and row.get("session_id")
        }
        frustration_by_session = {
            str(row.get("session_id")): row
            for row in frustration_rows
            if isinstance(row, dict) and row.get("session_id")
        }

        prompts: list[str] = []
        points: list[dict[str, Any]] = []
        for index, row in enumerate(query_runs, start=1):
            if not isinstance(row, dict):
                continue
            prompt = str(row.get("prompt") or "").strip()
            session_id = str(row.get("session_id") or "").strip()
            if not prompt or not session_id:
                continue
            response_text = str(row.get("response") or "")
            scenario_type = str(row.get("scenario_type") or "unknown")
            tool_eval = tool_by_session.get(session_id, {})
            frustration_eval = frustration_by_session.get(session_id, {})
            notes: list[str] = []
            if scenario_type == "unsupported_booking":
                notes.append("planning_only")
            elif scenario_type == "current_info":
                notes.append("current_info")
            else:
                notes.append("planning")

            expected_refusal = scenario_type == "unsupported_booking" or _expected_refusal(prompt)
            actual_refusal = _actual_refusal(response_text, notes)
            confusion_label = _confusion_label(expected_refusal=expected_refusal, actual_refusal=actual_refusal)
            success_label, success_score = _success_from_confusion_label(
                confusion_label,
                response_text=response_text,
                notes=notes,
            )

            if str(tool_eval.get("tool_usage_label") or "unknown") == "incorrect":
                success_label = "partial" if success_label == "works" else success_label
                success_score = min(success_score, 0.5)
            if str(frustration_eval.get("label") or "unknown") == "frustrated":
                success_label = "partial" if success_label == "works" else success_label
                success_score = min(success_score, 0.5)

            prompts.append(prompt)
            points.append(
                {
                    "id": index,
                    "prompt": prompt,
                    "category": scenario_type,
                    "expected_behavior": "planning_only" if expected_refusal else "normal_response",
                    "response": response_text,
                    "session_id": session_id,
                    "success_label": success_label,
                    "success_score": success_score,
                    "tool_hints": [str(item) for item in tool_eval.get("observed_tool_names", []) if item],
                    "notes": notes,
                    "source": "corpus",
                    "expected_refusal": expected_refusal,
                    "actual_refusal": actual_refusal,
                    "confusion_label": confusion_label,
                }
            )

        if not prompts:
            return {}

        payload = self._build_embedding_payload(
            corpus_id="evaluation",
            dataset_name="evaluation-corpus",
            prompts=prompts,
            points=points,
        )
        self._embedding_payload_cache["evaluation"] = payload
        return payload

    def _embedding_payload_for_corpus(self, corpus_id: str) -> dict[str, Any]:
        if corpus_id == "boundary":
            return self._boundary_embedding_payload()
        if corpus_id == "evaluation":
            return self._evaluation_embedding_payload()
        return {}

    def corpus_file_path(self, corpus_id: str) -> Path | None:
        corpus_files = {
            "evaluation": EVALS_DIR / "query_corpus.json",
            "boundary": EVALS_DIR / "boundary_prompt_corpus.json",
        }
        return corpus_files.get(corpus_id)

    def _load_span_rows(
        self,
        *,
        root_only: bool,
        limit: int,
    ) -> tuple[list[dict[str, Any]], bool, str | None]:
        try:
            rows = _rows_from_dataframe(
                self._client().spans.get_spans_dataframe(
                    project_name=self.settings.phoenix_project_name,
                    root_spans_only=root_only,
                    limit=limit,
                )
            )
            return rows, True, None
        except Exception as exc:
            filename = "root_spans.json" if root_only else "spans.json"
            fallback_rows = self._load_artifact_rows(filename, default=[])
            message = f"Phoenix unavailable. Showing cached data from artifacts/{filename}. ({exc})"
            return fallback_rows, False, message

    def _query_runs_by_session(self) -> dict[str, dict[str, Any]]:
        runs = self._load_artifact_rows("query_runs.json", default=[])
        return {
            str(row.get("session_id")): row
            for row in runs
            if isinstance(row, dict) and row.get("session_id")
        }

    def _artifact_overview_counts(self) -> tuple[int, int]:
        query_runs = self._load_artifact_rows("query_runs.json", default=[])
        session_ids = {
            str(row.get("session_id"))
            for row in query_runs
            if isinstance(row, dict) and row.get("session_id")
        }
        if not query_runs:
            return 0, 0

        root_rows = self._load_artifact_rows("root_spans.json", default=[])
        latest_trace_ids_by_session: dict[str, tuple[str, datetime]] = {}
        for row in root_rows:
            if not isinstance(row, dict):
                continue
            session_id = _session_id_from_row(row)
            trace_id = str(row.get("context.trace_id") or "")
            started_at = _parse_datetime(row.get("start_time"))
            if not session_id or session_id not in session_ids or not trace_id or not started_at:
                continue
            current = latest_trace_ids_by_session.get(session_id)
            if current is None or started_at > current[1]:
                latest_trace_ids_by_session[session_id] = (trace_id, started_at)

        span_rows = self._load_artifact_rows("spans.json", default=[])
        selected_trace_ids = {trace_id for trace_id, _ in latest_trace_ids_by_session.values()}
        if selected_trace_ids:
            matched_span_rows = [
                row
                for row in span_rows
                if isinstance(row, dict) and str(row.get("context.trace_id") or "") in selected_trace_ids
            ]
            return len(selected_trace_ids), len(matched_span_rows)

        matched_span_rows = [
            row
            for row in span_rows
            if isinstance(row, dict) and _session_id_from_row(row) in session_ids
        ]
        return len(query_runs), len(matched_span_rows or span_rows)

    def _evaluation_rows(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        frustration_rows = self._load_artifact_rows("user_frustration_evaluations.json", default=[])
        tool_rows = self._load_artifact_rows("tool_usage_evaluations.json", default=[])
        return frustration_rows, tool_rows

    def _trace_item_from_rows(
        self,
        *,
        trace_id: str,
        root_row: dict[str, Any],
        rows: list[dict[str, Any]],
        query_runs_by_session: dict[str, dict[str, Any]],
    ) -> TraceListItem:
        session_id = _session_id_from_row(root_row)
        query_run = query_runs_by_session.get(session_id or "")
        prompt_preview = None
        if query_run:
            prompt_preview = _truncate(query_run.get("prompt"))
        if not prompt_preview:
            prompt_preview = _prompt_from_row(root_row)
        return TraceListItem(
            trace_id=trace_id,
            span_id=str(root_row.get("span_id") or root_row.get("context.span_id") or ""),
            session_id=session_id,
            name=str(root_row.get("name") or "trace"),
            prompt_preview=prompt_preview,
            start_time=_format_datetime(root_row.get("start_time")),
            end_time=_format_datetime(root_row.get("end_time")),
            status_code=_truncate(root_row.get("status_code"), limit=32),
            span_count=len(rows),
            llm_span_count=_llm_span_count(rows),
            tool_names=_tool_names_from_rows(rows),
            phoenix_url=_phoenix_trace_url(
                self.settings.phoenix_base_url,
                self.settings.phoenix_project_name,
                trace_id,
            ),
        )

    def get_traces(self, *, limit: int = 12) -> TraceListResponse:
        root_rows, from_phoenix, message = self._load_span_rows(root_only=True, limit=max(limit * 3, 20))
        all_rows, _, fallback_message = self._load_span_rows(root_only=False, limit=max(limit * 20, 200))
        grouped_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in all_rows:
            trace_id = str(row.get("context.trace_id") or "")
            if trace_id:
                grouped_rows[trace_id].append(row)

        query_runs_by_session = self._query_runs_by_session()
        items: list[TraceListItem] = []
        for row in root_rows:
            trace_id = str(row.get("context.trace_id") or "")
            if not trace_id:
                continue
            trace_rows = grouped_rows.get(trace_id, [row])
            items.append(
                self._trace_item_from_rows(
                    trace_id=trace_id,
                    root_row=row,
                    rows=trace_rows,
                    query_runs_by_session=query_runs_by_session,
                )
            )

        items.sort(key=lambda item: item.start_time or "", reverse=True)
        combined_message = message or fallback_message
        return TraceListResponse(
            available=from_phoenix or bool(items),
            message=combined_message,
            traces=items[:limit],
        )

    def get_trace_detail(self, trace_id: str) -> TraceDetail:
        if not trace_id:
            return TraceDetail(available=False, message="Trace id is required.")

        root_rows, from_phoenix, message = self._load_span_rows(root_only=True, limit=100)
        all_rows, _, fallback_message = self._load_span_rows(root_only=False, limit=500)
        trace_rows = [row for row in all_rows if str(row.get("context.trace_id") or "") == trace_id]
        if not trace_rows:
            return TraceDetail(
                available=False,
                message=message or fallback_message or "Trace not found.",
            )

        root_row = next(
            (row for row in root_rows if str(row.get("context.trace_id") or "") == trace_id),
            trace_rows[0],
        )
        query_runs_by_session = self._query_runs_by_session()
        trace_item = self._trace_item_from_rows(
            trace_id=trace_id,
            root_row=root_row,
            rows=trace_rows,
            query_runs_by_session=query_runs_by_session,
        )

        span_summaries = [
            SpanSummary(
                span_id=str(row.get("span_id") or row.get("context.span_id") or ""),
                parent_id=_truncate(row.get("parent_id"), limit=64),
                name=str(row.get("name") or "span"),
                span_kind=_truncate(row.get("attributes.openinference.span.kind") or row.get("span_kind"), limit=32),
                status_code=_truncate(row.get("status_code"), limit=32),
                start_time=_format_datetime(row.get("start_time")),
                end_time=_format_datetime(row.get("end_time")),
                duration_ms=_duration_ms(row.get("start_time"), row.get("end_time")),
                input_preview=_input_preview(row),
                output_preview=_output_preview(row),
                error_message=_error_message(row),
                tool_name=str(row.get("name")) if str(row.get("name") or "") in TOOL_NAMES else None,
            )
            for row in sorted(trace_rows, key=lambda item: str(item.get("start_time") or ""))
        ]

        frustration_rows, tool_rows = self._evaluation_rows()
        evaluations: list[EvaluationResult] = []
        for kind, rows in (("user_frustration", frustration_rows), ("tool_usage", tool_rows)):
            for row in rows:
                if not isinstance(row, dict):
                    continue
                row_session_id = row.get("session_id")
                row_span_id = row.get("span_id")
                if row_session_id and trace_item.session_id and row_session_id == trace_item.session_id:
                    evaluations.append(self._evaluation_result(kind, row))
                elif row_span_id and trace_item.span_id and row_span_id == trace_item.span_id:
                    evaluations.append(self._evaluation_result(kind, row))

        return TraceDetail(
            available=from_phoenix or True,
            message=message or fallback_message,
            trace=trace_item,
            spans=span_summaries,
            evaluations=evaluations,
        )

    def get_evaluation_summary(self) -> EvaluationSummary:
        payload = self._load_artifact_rows("evaluation_summary.json", default={})
        if not payload:
            return EvaluationSummary(
                available=False,
                message="Missing artifacts/evaluation_summary.json.",
            )
        total_queries = int(payload.get("total_queries") or 0)
        tool_usage_incorrect = int(payload.get("tool_usage_incorrect") or 0)
        frustrated_count = int(payload.get("frustrated_count") or 0)
        incorrect_rate = (tool_usage_incorrect / total_queries) if total_queries else None
        frustration_rate = (frustrated_count / total_queries) if total_queries else None
        return EvaluationSummary(
            available=True,
            project_name=payload.get("project_name"),
            total_queries=total_queries,
            tool_usage_incorrect=tool_usage_incorrect,
            frustrated_count=frustrated_count,
            incorrect_rate=incorrect_rate,
            frustration_rate=frustration_rate,
            frustrated_dataset_name=payload.get("frustrated_dataset_name"),
        )

    def _evaluation_result(self, kind: str, row: dict[str, Any]) -> EvaluationResult:
        return EvaluationResult(
            kind=kind,
            session_id=row.get("session_id"),
            span_id=row.get("span_id"),
            label=str(row.get("label") or "unknown"),
            score=float(row["score"]) if row.get("score") is not None else None,
            explanation=_truncate(row.get("explanation"), limit=320),
            prompt=_truncate(row.get("prompt")),
            scenario_type=row.get("scenario_type"),
            observed_tool_names=[
                str(item)
                for item in row.get("observed_tool_names", [])
                if item
            ],
        )

    def get_evaluation_results(self) -> EvaluationResultsResponse:
        frustration_rows, tool_rows = self._evaluation_rows()
        if not frustration_rows and not tool_rows:
            return EvaluationResultsResponse(
                available=False,
                message="Evaluation artifacts are missing.",
            )
        return EvaluationResultsResponse(
            available=True,
            user_frustration=[
                self._evaluation_result("user_frustration", row)
                for row in frustration_rows
                if isinstance(row, dict)
            ],
            tool_usage=[
                self._evaluation_result("tool_usage", row)
                for row in tool_rows
                if isinstance(row, dict)
            ],
        )

    def get_frustrated_interactions(self) -> FrustratedInteractionsResponse:
        rows = self._load_artifact_rows("frustrated_interactions.json", default=[])
        if not rows:
            return FrustratedInteractionsResponse(
                available=False,
                message="No frustrated interaction dataset was found.",
            )
        items = [
            FrustratedInteraction(
                session_id=str(row.get("session_id") or ""),
                span_id=row.get("span_id"),
                prompt=str(row.get("prompt") or ""),
                response=str(row.get("response") or ""),
                scenario_type=row.get("scenario_type"),
                label=str(row.get("label") or "unknown"),
                score=float(row["score"]) if row.get("score") is not None else None,
                explanation=_truncate(row.get("explanation"), limit=320),
            )
            for row in rows
            if isinstance(row, dict)
        ]
        return FrustratedInteractionsResponse(available=True, items=items)

    def get_architecture_content(self) -> ArchitectureContent:
        architecture_doc = _read_text(PRESENTATION_ROOT / "production_architecture.md")
        presentation_doc = _read_text(PRESENTATION_ROOT / "presentation.md")
        if not architecture_doc and not presentation_doc:
            return ArchitectureContent(
                available=False,
                message="Presentation assets are missing.",
            )

        mermaid_diagram = None
        if architecture_doc:
            match = MERMAID_BLOCK_RE.search(architecture_doc)
            if match:
                mermaid_diagram = match.group(1).strip()

        slide_flow = _load_markdown_bullets(presentation_doc or "")
        architecture_bullets = _load_markdown_bullets(architecture_doc or "")

        runtime_flow = [
            item
            for item in slide_flow
            if item.startswith(("Runtime", "Graph", "Tool", "Structured Tool Output"))
        ]
        observability_flow = [
            item
            for item in slide_flow
            if item.startswith(("Observe", "One Request As A Trace", "Trace Evidence"))
        ]
        evaluation_flow = [
            item
            for item in slide_flow
            if item.startswith(("Evaluate", "Test Corpus", "Evaluation Pipeline", "User Frustration", "Tool Routing", "Debugging Example"))
        ]

        production_tradeoffs = architecture_bullets or [
            "Send all agent traces to Phoenix through OTLP and keep async evaluation workers off the user-serving path.",
            "Use stateless API replicas behind a load balancer so the app scales horizontally.",
            "Apply trace sampling in production to balance observability detail and cost.",
        ]

        deck_path = PRESENTATION_ROOT / "slides-dist" / "index.html"
        return ArchitectureContent(
            available=True,
            mermaid_diagram=mermaid_diagram,
            runtime_flow=runtime_flow,
            observability_flow=observability_flow,
            evaluation_flow=evaluation_flow,
            production_tradeoffs=production_tradeoffs,
            deck_url=self.settings.presentation_deck_url,
            deck_path=str(deck_path),
        )

    def get_boundary_embeddings(self, corpus_id: str = "boundary") -> BoundaryEmbeddingResponse:
        payload = self._embedding_payload_for_corpus(corpus_id)
        if not payload:
            return BoundaryEmbeddingResponse(
                available=False,
                message=(
                    "Boundary embedding data is missing. Run `poetry run python scripts/run_boundary_tests.py` first."
                    if corpus_id == "boundary"
                    else "Evaluation embedding data could not be calculated."
                ),
            )

        return BoundaryEmbeddingResponse(
            available=True,
            generated_at=payload.get("generated_at"),
            dataset_name=payload.get("dataset_name"),
            embedding_model=payload.get("embedding_model"),
            dimensions=int(payload.get("dimensions") or 3),
            summary=BoundaryEmbeddingSummary(**payload.get("summary", {})),
            points=[
                BoundaryEmbeddingPoint(**row)
                for row in payload.get("points", [])
                if isinstance(row, dict)
            ],
            category_similarity_matrix=[
                BoundaryMatrixRow(
                    row=str(row.get("row") or ""),
                    values=[
                        BoundaryMatrixCell(
                            column=str(value.get("column") or ""),
                            similarity=float(value.get("similarity") or 0.0),
                        )
                        for value in row.get("values", [])
                        if isinstance(value, dict)
                    ],
                )
                for row in payload.get("category_similarity_matrix", [])
                if isinstance(row, dict)
            ],
        )

    def get_boundary_projection(self, request: BoundaryProjectionRequest) -> BoundaryProjectionResponse:
        payload = self._embedding_payload_for_corpus(request.corpus_id)
        if not payload:
            return BoundaryProjectionResponse(
                available=False,
                message="Embedding data is missing for the selected corpus.",
            )

        projection_basis = payload.get("projection_basis") or {}
        mean = projection_basis.get("mean")
        components = projection_basis.get("components")
        if not isinstance(mean, list) or not isinstance(components, list):
            return BoundaryProjectionResponse(
                available=False,
                message="Boundary embedding artifact does not contain projection basis data.",
            )
        if not self.settings.openai_api_key:
            return BoundaryProjectionResponse(
                available=False,
                message="OPENAI_API_KEY is required to project live prompts into the embedding space.",
            )

        embedding_model = payload.get("embedding_model") or "text-embedding-3-small"
        client = OpenAI(api_key=self.settings.openai_api_key)
        embedding = client.embeddings.create(model=embedding_model, input=[request.prompt]).data[0].embedding

        vector = np.asarray(embedding, dtype=float)
        mean_vector = np.asarray(mean, dtype=float)
        component_matrix = np.asarray(components, dtype=float)
        projected = (vector - mean_vector) @ component_matrix.T
        max_abs = float(np.max(np.abs(projected))) or 1e-9
        normalized = projected / max_abs

        expected_refusal = _expected_refusal(request.prompt)
        actual_refusal = _actual_refusal(request.response, request.notes)
        confusion_label = _confusion_label(
            expected_refusal=expected_refusal,
            actual_refusal=actual_refusal,
        )
        success_label, success_score = _success_from_confusion_label(
            confusion_label,
            response_text=request.response,
            notes=request.notes,
        )

        return BoundaryProjectionResponse(
            available=True,
            point=BoundaryEmbeddingPoint(
                id=int(datetime.now().timestamp() * 1000),
                prompt=request.prompt,
                category="live_prompt",
                corpus_id=request.corpus_id,
                expected_behavior="planning_only" if expected_refusal else "normal_response",
                response=request.response,
                session_id=request.session_id,
                success_label=success_label,
                success_score=success_score,
                tool_hints=request.tool_hints,
                notes=request.notes,
                source="live",
                expected_refusal=expected_refusal,
                actual_refusal=actual_refusal,
                confusion_label=confusion_label,
                coords={
                    "x": round(float(normalized[0]), 4),
                    "y": round(float(normalized[1]), 4),
                    "z": round(float(normalized[2]), 4),
                },
            ),
        )

    def get_overview(self) -> DemoOverview:
        summary = self.get_evaluation_summary()
        trace_count, total_spans = self._artifact_overview_counts()

        if trace_count == 0 and total_spans == 0:
            traces = self.get_traces(limit=12)
            trace_count = len(traces.traces)
            total_spans = sum(item.span_count for item in traces.traces)
            message = traces.message or summary.message
            available = traces.available or summary.available
        else:
            message = summary.message
            available = summary.available or trace_count > 0

        return DemoOverview(
            available=available,
            message=message,
            trace_count=trace_count,
            total_spans=total_spans,
            total_queries=summary.total_queries,
            tool_usage_incorrect=summary.tool_usage_incorrect,
            frustrated_count=summary.frustrated_count,
            incorrect_rate=summary.incorrect_rate,
            frustration_rate=summary.frustration_rate,
            phoenix_base_url=self.settings.phoenix_base_url,
            phoenix_project_name=self.settings.phoenix_project_name,
        )

    def get_corpora(self) -> CorpusManifest:
        query_rows = self._load_corpus_rows("query_corpus.json", default=[])
        boundary_rows = self._load_corpus_rows("boundary_prompt_corpus.json", default=[])
        corpora = [
            CorpusDescriptor(
                id="evaluation",
                label="Evaluation Corpus",
                description="The 10-query scripted set used for tool routing and user-frustration evaluation.",
                count=len(query_rows),
                prompts=[str(row.get("prompt") or "") for row in query_rows if isinstance(row, dict) and row.get("prompt")],
                session_ids=[
                    session_id_for_prompt(str(row.get("prompt") or ""))
                    for row in query_rows
                    if isinstance(row, dict) and row.get("prompt")
                ],
                download_url="/demo/corpora/evaluation/download",
            ),
            CorpusDescriptor(
                id="boundary",
                label="Boundary Corpus",
                description="The 50-prompt stress set for unsupported bookings, frustration, and refusal behavior.",
                count=len(boundary_rows),
                prompts=[str(row.get("prompt") or "") for row in boundary_rows if isinstance(row, dict) and row.get("prompt")],
                session_ids=[
                    session_id_for_prompt(str(row.get("prompt") or ""))
                    for row in boundary_rows
                    if isinstance(row, dict) and row.get("prompt")
                ],
                download_url="/demo/corpora/boundary/download",
            ),
        ]
        return CorpusManifest(available=True, corpora=corpora)
