from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from typing import Iterator

from travel_assistant.config import Settings

_OBSERVABILITY_LOCK = threading.Lock()
_OBSERVABILITY_CONFIGURED = False


def configure_observability(settings: Settings) -> None:
    global _OBSERVABILITY_CONFIGURED
    if not settings.tracing_enabled:
        return
    with _OBSERVABILITY_LOCK:
        if _OBSERVABILITY_CONFIGURED:
            return
        os.environ.setdefault("PHOENIX_COLLECTOR_ENDPOINT", settings.phoenix_collector_endpoint)
        os.environ.setdefault("PHOENIX_PROJECT_NAME", settings.phoenix_project_name)
        try:
            from openinference.instrumentation.langchain import LangChainInstrumentor
            from phoenix.otel import register
        except ImportError:
            return

        register(
            endpoint=settings.phoenix_collector_endpoint,
            project_name=settings.phoenix_project_name,
            protocol="http/protobuf",
            batch=True,
            verbose=False,
            auto_instrument=True,
        )
        try:
            LangChainInstrumentor().instrument()
        except Exception:
            pass
        _OBSERVABILITY_CONFIGURED = True


@contextmanager
def maybe_using_attributes(**attributes: object) -> Iterator[None]:
    try:
        from openinference.instrumentation import using_attributes
    except ImportError:
        yield
        return
    with using_attributes(**attributes):
        yield


@contextmanager
def maybe_suppress_tracing() -> Iterator[None]:
    try:
        from openinference.instrumentation import suppress_tracing
    except ImportError:
        yield
        return
    with suppress_tracing():
        yield
