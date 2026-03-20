from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="User prompt to send to the agent.")


class ChatResponse(BaseModel):
    response: str


class ChatSource(BaseModel):
    url: str
    label: str | None = None


class ChatUIResponse(BaseModel):
    response: str
    session_id: str
    sources: list[ChatSource] = Field(default_factory=list)
    tool_hints: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class DemoOverview(BaseModel):
    available: bool = True
    message: str | None = None
    trace_count: int = 0
    total_spans: int = 0
    total_queries: int = 0
    tool_usage_incorrect: int = 0
    frustrated_count: int = 0
    incorrect_rate: float | None = None
    frustration_rate: float | None = None
    phoenix_base_url: str | None = None
    phoenix_project_name: str | None = None


class CorpusDescriptor(BaseModel):
    id: str
    label: str
    description: str | None = None
    count: int = 0
    session_ids: list[str] = Field(default_factory=list)
    prompts: list[str] = Field(default_factory=list)
    download_url: str


class CorpusManifest(BaseModel):
    available: bool = True
    message: str | None = None
    corpora: list[CorpusDescriptor] = Field(default_factory=list)


class TraceListItem(BaseModel):
    trace_id: str
    span_id: str | None = None
    session_id: str | None = None
    name: str
    prompt_preview: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    status_code: str | None = None
    span_count: int = 0
    llm_span_count: int = 0
    tool_names: list[str] = Field(default_factory=list)
    phoenix_url: str | None = None


class SpanSummary(BaseModel):
    span_id: str
    parent_id: str | None = None
    name: str
    span_kind: str | None = None
    status_code: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    duration_ms: float | None = None
    input_preview: str | None = None
    output_preview: str | None = None
    error_message: str | None = None
    tool_name: str | None = None


class TraceListResponse(BaseModel):
    available: bool = True
    message: str | None = None
    traces: list[TraceListItem] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    kind: str
    session_id: str | None = None
    span_id: str | None = None
    label: str
    score: float | None = None
    explanation: str | None = None
    prompt: str | None = None
    scenario_type: str | None = None
    observed_tool_names: list[str] = Field(default_factory=list)


class TraceDetail(BaseModel):
    available: bool = True
    message: str | None = None
    trace: TraceListItem | None = None
    spans: list[SpanSummary] = Field(default_factory=list)
    evaluations: list[EvaluationResult] = Field(default_factory=list)


class EvaluationSummary(BaseModel):
    available: bool = True
    message: str | None = None
    project_name: str | None = None
    total_queries: int = 0
    tool_usage_incorrect: int = 0
    frustrated_count: int = 0
    incorrect_rate: float | None = None
    frustration_rate: float | None = None
    frustrated_dataset_name: str | None = None


class EvaluationResultsResponse(BaseModel):
    available: bool = True
    message: str | None = None
    user_frustration: list[EvaluationResult] = Field(default_factory=list)
    tool_usage: list[EvaluationResult] = Field(default_factory=list)


class FrustratedInteraction(BaseModel):
    session_id: str
    span_id: str | None = None
    prompt: str
    response: str
    scenario_type: str | None = None
    label: str
    score: float | None = None
    explanation: str | None = None


class FrustratedInteractionsResponse(BaseModel):
    available: bool = True
    message: str | None = None
    items: list[FrustratedInteraction] = Field(default_factory=list)


class ArchitectureContent(BaseModel):
    available: bool = True
    message: str | None = None
    mermaid_diagram: str | None = None
    runtime_flow: list[str] = Field(default_factory=list)
    observability_flow: list[str] = Field(default_factory=list)
    evaluation_flow: list[str] = Field(default_factory=list)
    production_tradeoffs: list[str] = Field(default_factory=list)
    deck_url: str | None = None
    deck_path: str | None = None


class EmbeddingCoordinate(BaseModel):
    x: float
    y: float
    z: float


class BoundaryEmbeddingPoint(BaseModel):
    id: int
    prompt: str
    category: str
    expected_behavior: str
    response: str
    session_id: str
    success_label: str
    success_score: float
    tool_hints: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    source: str = "corpus"
    expected_refusal: bool | None = None
    actual_refusal: bool | None = None
    confusion_label: str | None = None
    coords: EmbeddingCoordinate


class BoundaryMatrixCell(BaseModel):
    column: str
    similarity: float


class BoundaryMatrixRow(BaseModel):
    row: str
    values: list[BoundaryMatrixCell] = Field(default_factory=list)


class BoundaryEmbeddingSummary(BaseModel):
    total_prompts: int = 0
    worked: int = 0
    partial: int = 0
    failed: int = 0
    success_rate: float | None = None


class BoundaryEmbeddingResponse(BaseModel):
    available: bool = True
    message: str | None = None
    generated_at: str | None = None
    dataset_name: str | None = None
    embedding_model: str | None = None
    dimensions: int = 3
    summary: BoundaryEmbeddingSummary = Field(default_factory=BoundaryEmbeddingSummary)
    points: list[BoundaryEmbeddingPoint] = Field(default_factory=list)
    category_similarity_matrix: list[BoundaryMatrixRow] = Field(default_factory=list)


class BoundaryProjectionRequest(BaseModel):
    prompt: str
    response: str
    session_id: str
    notes: list[str] = Field(default_factory=list)
    tool_hints: list[str] = Field(default_factory=list)


class BoundaryProjectionResponse(BaseModel):
    available: bool = True
    message: str | None = None
    point: BoundaryEmbeddingPoint | None = None


class WebSearchInput(BaseModel):
    query: str = Field(min_length=3, description="Search query for current information.")
    max_results: int = Field(default=5, ge=1, le=10)


class AttractionSearchInput(BaseModel):
    destination: str = Field(min_length=2)
    interests: list[str] = Field(default_factory=list)
    max_results: int = Field(default=5, ge=1, le=10)

    @field_validator("interests")
    @classmethod
    def clean_interests(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item and item.strip()]


class AttractionResult(BaseModel):
    name: str
    category: str
    summary: str
    estimated_cost: str
    rationale: str
    source_url: str


class AttractionSearchOutput(BaseModel):
    destination: str
    attractions: list[AttractionResult] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class SearchResult(BaseModel):
    title: str
    snippet: str
    source_url: str


class WebSearchOutput(BaseModel):
    query: str
    results: list[SearchResult] = Field(default_factory=list)


class ScriptedQuery(BaseModel):
    prompt: str
    expected_primary_tool: Literal["search_attractions", "search_web", "none"]
    scenario_type: str
