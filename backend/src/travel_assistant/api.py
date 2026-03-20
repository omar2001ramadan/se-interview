from __future__ import annotations

import re
from urllib.parse import urlparse
import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage

from travel_assistant.config import get_settings
from travel_assistant.demo_data import DemoDataService
from travel_assistant.graph import build_agent
from travel_assistant.observability import configure_observability, maybe_using_attributes
from travel_assistant.query_loader import session_id_for_prompt
from travel_assistant.schemas import (
    ArchitectureContent,
    BoundaryEmbeddingResponse,
    BoundaryProjectionRequest,
    BoundaryProjectionResponse,
    ChatRequest,
    ChatResponse,
    ChatSource,
    ChatUIResponse,
    CorpusManifest,
    DemoOverview,
    EvaluationResultsResponse,
    EvaluationSummary,
    FrustratedInteractionsResponse,
    TraceDetail,
    TraceListResponse,
)

load_dotenv()

MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)]+")
BOOKING_KEYWORDS = ("book", "booking", "reserve", "reservation", "ticket", "tickets", "hotel", "flight")
PLANNING_ONLY_PATTERNS = ("can't book", "cannot book", "can't reserve", "cannot reserve", "cannot complete the booking")


def _source_label(url: str) -> str:
    hostname = urlparse(url).netloc.removeprefix("www.")
    return hostname or "Source"


def _extract_sources(response_text: str) -> list[ChatSource]:
    sources: list[ChatSource] = []
    seen_urls: set[str] = set()
    for label, url in MARKDOWN_LINK_RE.findall(response_text):
        if url in seen_urls:
            continue
        seen_urls.add(url)
        sources.append(ChatSource(url=url, label=label.strip() or _source_label(url)))
    for url in URL_RE.findall(response_text):
        if url in seen_urls:
            continue
        seen_urls.add(url)
        sources.append(ChatSource(url=url, label=_source_label(url)))
    return sources


def _append_source(
    sources: list[ChatSource],
    seen_urls: set[str],
    *,
    url: str,
    label: str | None = None,
) -> None:
    if not url or url in seen_urls:
        return
    seen_urls.add(url)
    sources.append(ChatSource(url=url, label=(label or _source_label(url))))


def _extract_sources_from_tool_messages(messages: list[object]) -> list[ChatSource]:
    sources: list[ChatSource] = []
    seen_urls: set[str] = set()
    for message in messages:
        content = getattr(message, "content", None)
        if not isinstance(content, str):
            continue
        try:
            payload = json.loads(content)
        except Exception:
            continue
        if isinstance(payload, dict):
            if isinstance(payload.get("results"), list):
                for item in payload["results"]:
                    if not isinstance(item, dict):
                        continue
                    _append_source(
                        sources,
                        seen_urls,
                        url=str(item.get("source_url") or ""),
                        label=str(item.get("title") or "") or None,
                    )
            if isinstance(payload.get("attractions"), list):
                for item in payload["attractions"]:
                    if not isinstance(item, dict):
                        continue
                    _append_source(
                        sources,
                        seen_urls,
                        url=str(item.get("source_url") or ""),
                        label=str(item.get("name") or "") or None,
                    )
    return sources


def _extract_tool_hints(messages: list[object]) -> list[str]:
    tool_hints: list[str] = []
    for message in messages:
        tool_calls = getattr(message, "tool_calls", None) or []
        for tool_call in tool_calls:
            tool_name = str(tool_call.get("name", "")).strip()
            if tool_name and tool_name not in tool_hints:
                tool_hints.append(tool_name)
    return tool_hints


def _extract_notes(prompt: str, response_text: str, tool_hints: list[str]) -> list[str]:
    notes: list[str] = []
    prompt_lower = prompt.lower()
    response_lower = response_text.lower()
    if any(keyword in prompt_lower for keyword in BOOKING_KEYWORDS) and any(
        pattern in response_lower for pattern in PLANNING_ONLY_PATTERNS
    ):
        notes.append("planning_only")
    if "search_web" in tool_hints:
        notes.append("current_info")
    elif "search_attractions" in tool_hints:
        notes.append("planning")
    return notes


def _build_ui_response(*, prompt: str, session_id: str, agent_result: dict) -> ChatUIResponse:
    messages = agent_result["messages"]
    response_text = str(messages[-1].content)
    tool_hints = _extract_tool_hints(messages)
    tool_sources = _extract_sources_from_tool_messages(messages)
    response_sources = _extract_sources(response_text)
    return ChatUIResponse(
        response=response_text,
        session_id=session_id,
        sources=tool_sources or response_sources,
        tool_hints=tool_hints,
        notes=_extract_notes(prompt, response_text, tool_hints),
    )


def create_app(agent_executor=None, demo_service=None) -> FastAPI:
    settings = get_settings()
    configure_observability(settings)

    app = FastAPI(
        title="Travel Assistant Agent API",
        description="Travel planning assistant backed by LangGraph, DuckDuckGo, and Arize Phoenix",
        version="0.2.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.agent = agent_executor
    app.state.demo_service = demo_service or DemoDataService(settings)
    app.state.settings = settings

    def run_agent(prompt: str) -> tuple[str, dict]:
        session_id = session_id_for_prompt(prompt)
        if app.state.agent is None:
            app.state.agent = build_agent(app.state.settings)
        with maybe_using_attributes(
            session_id=session_id,
            metadata={"route": "/chat", "project": settings.phoenix_project_name},
        ):
            result = app.state.agent.invoke({"messages": [HumanMessage(content=prompt)]})
        return session_id, result

    @app.post("/chat", response_model=ChatResponse)
    def chat(request: ChatRequest) -> ChatResponse:
        _, result = run_agent(request.message)
        return ChatResponse(response=result["messages"][-1].content)

    @app.post("/chat/ui", response_model=ChatUIResponse)
    def chat_ui(request: ChatRequest) -> ChatUIResponse:
        session_id, result = run_agent(request.message)
        return _build_ui_response(
            prompt=request.message,
            session_id=session_id,
            agent_result=result,
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/demo/overview", response_model=DemoOverview)
    def demo_overview() -> DemoOverview:
        return app.state.demo_service.get_overview()

    @app.get("/demo/corpora", response_model=CorpusManifest)
    def demo_corpora() -> CorpusManifest:
        return app.state.demo_service.get_corpora()

    @app.get("/demo/corpora/{corpus_id}/download")
    def download_corpus(corpus_id: str):
        file_path = app.state.demo_service.corpus_file_path(corpus_id)
        if file_path is None:
            raise HTTPException(status_code=404, detail="Unknown corpus.")
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Corpus file not found.")
        return FileResponse(file_path, media_type="application/json", filename=file_path.name)

    @app.get("/demo/traces", response_model=TraceListResponse)
    def demo_traces() -> TraceListResponse:
        return app.state.demo_service.get_traces()

    @app.get("/demo/traces/{trace_id}", response_model=TraceDetail)
    def demo_trace_detail(trace_id: str) -> TraceDetail:
        return app.state.demo_service.get_trace_detail(trace_id)

    @app.get("/demo/evaluations/summary", response_model=EvaluationSummary)
    def demo_evaluations_summary() -> EvaluationSummary:
        return app.state.demo_service.get_evaluation_summary()

    @app.get("/demo/evaluations/results", response_model=EvaluationResultsResponse)
    def demo_evaluations_results() -> EvaluationResultsResponse:
        return app.state.demo_service.get_evaluation_results()

    @app.get("/demo/evaluations/frustrated", response_model=FrustratedInteractionsResponse)
    def demo_evaluations_frustrated() -> FrustratedInteractionsResponse:
        return app.state.demo_service.get_frustrated_interactions()

    @app.get("/demo/architecture", response_model=ArchitectureContent)
    def demo_architecture() -> ArchitectureContent:
        return app.state.demo_service.get_architecture_content()

    @app.get("/demo/boundaries", response_model=BoundaryEmbeddingResponse)
    def demo_boundaries(corpus_id: str = "boundary") -> BoundaryEmbeddingResponse:
        return app.state.demo_service.get_boundary_embeddings(corpus_id)

    @app.post("/demo/boundaries/project", response_model=BoundaryProjectionResponse)
    def demo_boundary_projection(request: BoundaryProjectionRequest) -> BoundaryProjectionResponse:
        return app.state.demo_service.get_boundary_projection(request)

    return app


app = create_app()
