from __future__ import annotations

import csv
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("OTEL_SDK_DISABLED", "true")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from phoenix.client import Client
from phoenix.evals import (
    USER_FRUSTRATION_PROMPT_RAILS_MAP,
    USER_FRUSTRATION_PROMPT_TEMPLATE,
    OpenAIModel,
    llm_classify,
)

from evals.tool_usage import evaluate_tool_usage
from travel_assistant.config import get_settings
from travel_assistant.query_loader import load_query_corpus, session_id_for_prompt

TOOL_NAMES = {"search_attractions", "search_web"}


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
        return dataframe
    return list(dataframe or [])


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=sorted(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _load_query_runs() -> list[dict[str, Any]]:
    query_runs_path = Path("artifacts/query_runs.json")
    if not query_runs_path.exists():
        raise FileNotFoundError(
            "Missing artifacts/query_runs.json. Run `python3 -m poetry run python scripts/run_queries.py` first."
        )
    return json.loads(query_runs_path.read_text())


def _row_contains_token(row: dict[str, Any], token: str) -> bool:
    return token in json.dumps(row, default=str)


def _find_matching_root_span(
    root_span_rows: list[dict[str, Any]],
    *,
    session_id: str,
    prompt: str,
) -> dict[str, Any] | None:
    for row in root_span_rows:
        if _row_contains_token(row, session_id):
            return row
    for row in root_span_rows:
        if _row_contains_token(row, prompt):
            return row
    return None


def _extract_tool_names(span_rows: list[dict[str, Any]], *, session_id: str, prompt: str) -> list[str]:
    observed: list[str] = []
    for row in span_rows:
        if not (_row_contains_token(row, session_id) or _row_contains_token(row, prompt)):
            continue
        name = str(row.get("name", "")).strip()
        if name in TOOL_NAMES and name not in observed:
            observed.append(name)
    return observed


def _conversation_text(prompt: str, response: str) -> str:
    return f"User: {prompt}\nAssistant: {response}"


def _annotate_span(
    client: Client,
    *,
    span_id: str | None,
    annotation_name: str,
    annotator_kind: str,
    label: str,
    score: float,
    explanation: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    if not span_id:
        return
    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name=annotation_name,
        annotator_kind=annotator_kind,
        label=label,
        score=score,
        explanation=explanation,
        metadata=metadata,
        sync=True,
    )


def _evaluate_user_frustration(
    records: list[dict[str, Any]],
    *,
    settings,
) -> list[dict[str, Any]]:
    if not settings.openai_api_key:
        return []
    if not records:
        return []
    dataframe = pd.DataFrame(
        [{"conversation": record["conversation"]} for record in records],
        index=[record["session_id"] for record in records],
    )
    model = OpenAIModel(
        model=settings.openai_eval_model,
        api_key=settings.openai_api_key,
        temperature=0.0,
    )
    results = llm_classify(
        dataframe,
        model=model,
        template=USER_FRUSTRATION_PROMPT_TEMPLATE,
        rails=list(USER_FRUSTRATION_PROMPT_RAILS_MAP.values()),
        provide_explanation=True,
        run_sync=True,
        exit_on_error=False,
    )
    output = []
    for record, (_, evaluation) in zip(records, results.iterrows()):
        label = evaluation.get("label") or "NOT_PARSABLE"
        explanation = evaluation.get("explanation") or "No explanation provided."
        score = 0.0 if label == "frustrated" else 1.0
        output.append(
            {
                "session_id": record["session_id"],
                "span_id": record["span_id"],
                "prompt": record["prompt"],
                "response": record["response"],
                "scenario_type": record["scenario_type"],
                "label": label,
                "score": score,
                "explanation": explanation,
            }
        )
    return output


def _create_frustrated_dataset(
    client: Client,
    frustrated_rows: list[dict[str, Any]],
) -> str | None:
    if not frustrated_rows:
        return None
    dataset_name = f"frustrated-interactions-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    examples = []
    for row in frustrated_rows:
        if not row.get("span_id"):
            continue
        examples.append(
            {
                "input": {"prompt": row["prompt"]},
                "output": {"response": row["response"]},
                "metadata": {
                    "scenario_type": row["scenario_type"],
                    "user_frustration_label": row["label"],
                },
                "span_id": row["span_id"],
            }
        )
    if not examples:
        return None
    client.datasets.create_dataset(
        name=dataset_name,
        examples=examples,
        dataset_description="Frustrated travel assistant interactions derived from Phoenix traces.",
    )
    return dataset_name


def main() -> None:
    settings = get_settings()
    client = Client(base_url=settings.phoenix_base_url)

    query_runs = _load_query_runs()
    corpus = load_query_corpus(settings.query_corpus_path)
    expected_tool_by_prompt = {
        item.prompt: item.expected_primary_tool
        for item in corpus
    }

    span_rows = _rows_from_dataframe(
        client.spans.get_spans_dataframe(
            project_name=settings.phoenix_project_name,
            limit=max(200, len(query_runs) * 20),
        )
    )
    root_span_rows = _rows_from_dataframe(
        client.spans.get_spans_dataframe(
            project_name=settings.phoenix_project_name,
            root_spans_only=True,
            limit=max(50, len(query_runs) * 5),
        )
    )

    _write_json(Path("artifacts/spans.json"), span_rows)
    _write_csv(Path("artifacts/spans.csv"), span_rows)
    _write_json(Path("artifacts/root_spans.json"), root_span_rows)

    evaluation_records = []
    for run in query_runs:
        session_id = run.get("session_id") or session_id_for_prompt(run["prompt"])
        root_span = _find_matching_root_span(
            root_span_rows,
            session_id=session_id,
            prompt=run["prompt"],
        )
        observed_tool_names = _extract_tool_names(
            span_rows,
            session_id=session_id,
            prompt=run["prompt"],
        )
        tool_usage = evaluate_tool_usage(
            expected_tool_by_prompt[run["prompt"]],
            observed_tool_names,
        )
        span_id = None if root_span is None else str(root_span.get("span_id") or root_span.get("context.span_id"))
        evaluation_record = {
            "session_id": session_id,
            "span_id": span_id,
            "prompt": run["prompt"],
            "response": run["response"],
            "scenario_type": run["scenario_type"],
            "expected_primary_tool": run["expected_primary_tool"],
            "observed_tool_names": observed_tool_names,
            "conversation": _conversation_text(run["prompt"], run["response"]),
            "tool_usage_label": tool_usage.label,
            "tool_usage_score": tool_usage.score,
            "tool_usage_explanation": tool_usage.explanation,
        }
        evaluation_records.append(evaluation_record)
        _annotate_span(
            client,
            span_id=span_id,
            annotation_name="tool_usage_correctness",
            annotator_kind="CODE",
            label=tool_usage.label,
            score=tool_usage.score,
            explanation=tool_usage.explanation,
            metadata={
                "expected_primary_tool": run["expected_primary_tool"],
                "observed_tool_names": observed_tool_names,
                "scenario_type": run["scenario_type"],
            },
        )

    _write_json(Path("artifacts/tool_usage_evaluations.json"), evaluation_records)

    frustration_results = _evaluate_user_frustration(evaluation_records, settings=settings)
    for result in frustration_results:
        _annotate_span(
            client,
            span_id=result["span_id"],
            annotation_name="user_frustration",
            annotator_kind="LLM",
            label=result["label"],
            score=result["score"],
            explanation=result["explanation"],
            metadata={"scenario_type": result["scenario_type"]},
        )

    _write_json(Path("artifacts/user_frustration_evaluations.json"), frustration_results)

    frustrated_rows = [row for row in frustration_results if row["label"] == "frustrated"]
    _write_json(Path("artifacts/frustrated_interactions.json"), frustrated_rows)
    dataset_name = _create_frustrated_dataset(client, frustrated_rows)
    _write_json(
        Path("artifacts/evaluation_summary.json"),
        {
            "project_name": settings.phoenix_project_name,
            "total_queries": len(query_runs),
            "tool_usage_incorrect": sum(1 for row in evaluation_records if row["tool_usage_label"] == "incorrect"),
            "frustrated_count": len(frustrated_rows),
            "frustrated_dataset_name": dataset_name,
        },
    )
    print("Exported spans, logged Phoenix annotations, and generated evaluation artifacts.")
    if dataset_name:
        print(f"Created Phoenix dataset: {dataset_name}")
    else:
        print("No frustrated interactions were classified; dataset creation was skipped.")


if __name__ == "__main__":
    main()
