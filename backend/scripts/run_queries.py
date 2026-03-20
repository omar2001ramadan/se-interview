from __future__ import annotations

import json
from pathlib import Path

import httpx

from travel_assistant.config import get_settings
from travel_assistant.query_loader import load_query_corpus, session_id_for_prompt


def main() -> None:
    settings = get_settings()
    corpus = load_query_corpus(settings.query_corpus_path)
    base_url = "http://localhost:8000"
    results = []
    with httpx.Client(base_url=base_url, timeout=60.0) as client:
        for index, query in enumerate(corpus, start=1):
            response = client.post("/chat", json={"message": query.prompt})
            response.raise_for_status()
            payload = response.json()
            results.append(
                {
                    "id": index,
                    "prompt": query.prompt,
                    "session_id": session_id_for_prompt(query.prompt),
                    "scenario_type": query.scenario_type,
                    "expected_primary_tool": query.expected_primary_tool,
                    "response": payload["response"],
                }
            )
            print(f"[{index}/{len(corpus)}] {query.scenario_type}: {query.prompt}")

    output_path = Path("artifacts/query_runs.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2))
    print(f"Saved query responses to {output_path}")


if __name__ == "__main__":
    main()
