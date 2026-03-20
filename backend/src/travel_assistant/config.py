from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

LOCAL_CORS_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
)


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_csv_list(value: str | None, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default
    items = tuple(item.strip().rstrip("/") for item in value.split(",") if item.strip())
    return items or default


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    openai_eval_model: str
    openai_temperature: float
    tracing_enabled: bool
    phoenix_project_name: str
    phoenix_base_url: str
    phoenix_collector_endpoint: str
    search_region: str
    query_corpus_path: str
    cors_allowed_origins: tuple[str, ...]
    presentation_deck_url: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    phoenix_base_url = os.getenv("PHOENIX_BASE_URL", "http://localhost:6006").rstrip("/")
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        openai_eval_model=os.getenv("OPENAI_EVAL_MODEL", "gpt-4o-mini"),
        openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
        tracing_enabled=_as_bool(os.getenv("TRACING_ENABLED"), True),
        phoenix_project_name=os.getenv("PHOENIX_PROJECT_NAME", "travel-assistant-assessment"),
        phoenix_base_url=phoenix_base_url,
        phoenix_collector_endpoint=os.getenv(
            "PHOENIX_COLLECTOR_ENDPOINT",
            f"{phoenix_base_url}/v1/traces",
        ),
        search_region=os.getenv("SEARCH_REGION", "wt-wt"),
        query_corpus_path=os.getenv("QUERY_CORPUS_PATH", "evals/query_corpus.json"),
        cors_allowed_origins=_as_csv_list(
            os.getenv("CORS_ALLOWED_ORIGINS"),
            LOCAL_CORS_ORIGINS,
        ),
        presentation_deck_url=os.getenv("PRESENTATION_DECK_URL", "http://localhost:4173").rstrip("/"),
    )
