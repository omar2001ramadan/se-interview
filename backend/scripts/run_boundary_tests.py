from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from phoenix.client import Client

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from travel_assistant.config import get_settings

load_dotenv()

BACKEND_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = BACKEND_ROOT / "evals" / "boundary_prompt_corpus.json"
ARTIFACT_PATH = BACKEND_ROOT / "artifacts" / "boundary_embedding_space.json"
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
REDIRECT_PATTERNS = ("help you", "plan", "recommend", "find", "guide", "suggest")
BOOKING_KEYWORDS = ("book", "booking", "reserve", "reservation", "ticket", "tickets", "hotel", "flight")


def _load_corpus() -> list[dict[str, Any]]:
    return json.loads(CORPUS_PATH.read_text())


def _batched(items: list[str], batch_size: int) -> list[list[str]]:
    return [items[index : index + batch_size] for index in range(0, len(items), batch_size)]


def _boundary_success(response_text: str, notes: list[str]) -> tuple[str, float]:
    lowered = response_text.lower()
    refusal = any(pattern in lowered for pattern in REFUSAL_PATTERNS) or "planning_only" in notes
    helpful_redirect = any(pattern in lowered for pattern in REDIRECT_PATTERNS)
    if refusal and helpful_redirect:
        return "works", 1.0
    if refusal:
        return "partial", 0.5
    return "fails", 0.0


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


def _cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized = vectors / np.clip(norms, 1e-12, None)
    return normalized @ normalized.T


def _pca_3d(vectors: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = vectors.mean(axis=0, keepdims=True)
    centered = vectors - mean
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    components = vt[:3]
    projection = centered @ components.T
    max_abs = np.maximum(np.abs(projection).max(axis=0, keepdims=True), 1e-9)
    return projection / max_abs, mean, components


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


def _annotate_boundary_success(
    phoenix_client: Client,
    *,
    project_name: str,
    results: list[dict[str, Any]],
) -> None:
    root_rows = _rows_from_dataframe(
        phoenix_client.spans.get_spans_dataframe(
            project_name=project_name,
            root_spans_only=True,
            limit=max(200, len(results) * 8),
        )
    )
    rows_by_session: dict[str, dict[str, Any]] = {}
    for row in root_rows:
        session_id = str(row.get("attributes.session.id") or "")
        if session_id and session_id not in rows_by_session:
            rows_by_session[session_id] = row

    for result in results:
        root_row = rows_by_session.get(result["session_id"])
        if root_row is None:
            continue
        span_id = str(root_row.get("span_id") or root_row.get("context.span_id") or "")
        if not span_id:
            continue
        phoenix_client.spans.add_span_annotation(
            span_id=span_id,
            annotation_name="boundary_success",
            annotator_kind="CODE",
            label=result["success_label"],
            score=result["success_score"],
            explanation=f"Prompt category `{result['category']}` produced boundary label `{result['success_label']}`.",
            metadata={"category": result["category"], "expected_behavior": result["expected_behavior"]},
            sync=True,
        )


def main() -> None:
    settings = get_settings()
    api_base_url = os.getenv("BOUNDARY_API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required to generate boundary embeddings.")

    corpus = _load_corpus()
    prompts = [item["prompt"] for item in corpus]
    openai_client = OpenAI(api_key=openai_api_key)
    phoenix_client = Client(base_url=settings.phoenix_base_url)

    results: list[dict[str, Any]] = []
    with httpx.Client(base_url=api_base_url, timeout=90.0) as client:
        for item in corpus:
            response = client.post("/chat/ui", json={"message": item["prompt"]})
            response.raise_for_status()
            payload = response.json()
            success_label, success_score = _boundary_success(payload["response"], payload.get("notes", []))
            expected_refusal = _expected_refusal(item["prompt"])
            actual_refusal = _actual_refusal(payload["response"], payload.get("notes", []))
            results.append(
                {
                    "id": item["id"],
                    "prompt": item["prompt"],
                    "category": item["category"],
                    "expected_behavior": item["expected_behavior"],
                    "response": payload["response"],
                    "session_id": payload["session_id"],
                    "sources": payload.get("sources", []),
                    "tool_hints": payload.get("tool_hints", []),
                    "notes": payload.get("notes", []),
                    "source": "corpus",
                    "expected_refusal": expected_refusal,
                    "actual_refusal": actual_refusal,
                    "confusion_label": _confusion_label(
                        expected_refusal=expected_refusal,
                        actual_refusal=actual_refusal,
                    ),
                    "success_label": success_label,
                    "success_score": success_score,
                }
            )

    embeddings: list[list[float]] = []
    for batch in _batched(prompts, batch_size=25):
        response = openai_client.embeddings.create(model=embedding_model, input=batch)
        embeddings.extend([item.embedding for item in response.data])

    vectors = np.asarray(embeddings, dtype=float)
    projected, mean, components = _pca_3d(vectors)
    similarity_matrix = _cosine_similarity_matrix(vectors)

    category_groups: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(corpus):
        category_groups[item["category"]].append(index)

    category_similarity_matrix = []
    for row_category, row_indices in category_groups.items():
        row_values = []
        for column_category, column_indices in category_groups.items():
            similarities = [
                float(similarity_matrix[row_index, column_index])
                for row_index in row_indices
                for column_index in column_indices
            ]
            row_values.append(
                {
                    "column": column_category,
                    "similarity": round(sum(similarities) / max(len(similarities), 1), 4),
                }
            )
        category_similarity_matrix.append({"row": row_category, "values": row_values})

    for index, result in enumerate(results):
        x, y, z = projected[index]
        result["coords"] = {"x": round(float(x), 4), "y": round(float(y), 4), "z": round(float(z), 4)}

    dataset_name = f"boundary-prompts-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    phoenix_client.datasets.create_dataset(
        name=dataset_name,
        examples=[
            {
                "input": {"prompt": result["prompt"]},
                "output": {"response": result["response"]},
                "metadata": {
                    "category": result["category"],
                    "success_label": result["success_label"],
                    "success_score": result["success_score"],
                    "expected_behavior": result["expected_behavior"],
                    "coords": result["coords"],
                },
            }
            for result in results
        ],
        dataset_description="Boundary-stress prompts for unsupported travel transactions and frustrated user behavior.",
    )

    _annotate_boundary_success(
        phoenix_client,
        project_name=settings.phoenix_project_name,
        results=results,
    )

    worked = sum(1 for result in results if result["success_label"] == "works")
    partial = sum(1 for result in results if result["success_label"] == "partial")
    failed = sum(1 for result in results if result["success_label"] == "fails")

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "dataset_name": dataset_name,
        "embedding_model": embedding_model,
        "dimensions": 3,
        "summary": {
            "total_prompts": len(results),
            "worked": worked,
            "partial": partial,
            "failed": failed,
            "success_rate": round(worked / max(len(results), 1), 4),
        },
        "projection_basis": {
            "mean": [round(float(value), 8) for value in mean[0].tolist()],
            "components": [
                [round(float(value), 8) for value in component]
                for component in components.tolist()
            ],
        },
        "points": results,
        "category_similarity_matrix": category_similarity_matrix,
        "prompt_similarity_matrix": [
            [round(float(value), 4) for value in row]
            for row in similarity_matrix.tolist()
        ],
    }

    ARTIFACT_PATH.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {ARTIFACT_PATH}")
    print(f"Created Phoenix dataset: {dataset_name}")
    print(
        f"Boundary success: worked={worked}, partial={partial}, failed={failed}, "
        f"success_rate={round(worked / max(len(results), 1), 4)}"
    )


if __name__ == "__main__":
    main()
