from __future__ import annotations

import hashlib
import json
from pathlib import Path

from travel_assistant.schemas import ScriptedQuery


def load_query_corpus(path: str) -> list[ScriptedQuery]:
    data = json.loads(Path(path).read_text())
    return [ScriptedQuery.model_validate(item) for item in data]


def session_id_for_prompt(prompt: str) -> str:
    digest = hashlib.sha1(prompt.encode("utf-8")).hexdigest()
    return f"travel-session-{digest[:16]}"
