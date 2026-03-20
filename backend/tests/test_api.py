from fastapi.testclient import TestClient

from travel_assistant.api import _build_ui_response, create_app
from travel_assistant.schemas import (
    ArchitectureContent,
    BoundaryEmbeddingPoint,
    BoundaryEmbeddingResponse,
    BoundaryProjectionResponse,
    BoundaryEmbeddingSummary,
    BoundaryMatrixCell,
    BoundaryMatrixRow,
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


class FakeAgent:
    def invoke(self, payload):
        message = payload["messages"][0].content
        ai_message = type(
            "Message",
            (),
            {
                "content": f"Echo: {message}",
                "tool_calls": [],
            },
        )()
        return {"messages": [ai_message]}


class FakeToolAgent:
    def invoke(self, payload):
        message = payload["messages"][0].content
        routed = type(
            "ToolDecision",
            (),
            {
                "content": "",
                "tool_calls": [{"name": "search_attractions", "args": {"destination": "Chicago"}}],
            },
        )()
        final = type(
            "FinalMessage",
            (),
            {
                "content": (
                    f"For {message}, start with the Riverwalk. "
                    "[Official Guide](https://example.com/guide)"
                ),
                "tool_calls": [],
            },
        )()
        return {"messages": [routed, final]}


class FakeDemoService:
    def get_overview(self):
        return DemoOverview(
            trace_count=10,
            total_spans=137,
            total_queries=10,
            tool_usage_incorrect=1,
            frustrated_count=2,
            incorrect_rate=0.1,
            frustration_rate=0.2,
            phoenix_base_url="http://localhost:6006",
            phoenix_project_name="travel-assistant-assessment",
        )

    def get_traces(self):
        return TraceListResponse(
            traces=[
                TraceListItem(
                    trace_id="trace-123",
                    span_id="span-123",
                    session_id="travel-session-123",
                    name="llm_call",
                    prompt_preview="Plan a day in Chicago",
                    span_count=5,
                    llm_span_count=2,
                    tool_names=["search_attractions"],
                    phoenix_url="http://localhost:6006/projects/demo/traces/trace-123",
                )
            ]
        )

    def get_trace_detail(self, trace_id: str):
        return TraceDetail(
            trace=TraceListItem(
                trace_id=trace_id,
                span_id="span-123",
                session_id="travel-session-123",
                name="llm_call",
                prompt_preview="Plan a day in Chicago",
                span_count=5,
                llm_span_count=2,
                tool_names=["search_attractions"],
                phoenix_url="http://localhost:6006/projects/demo/traces/trace-123",
            ),
            spans=[
                SpanSummary(
                    span_id="span-123",
                    name="search_attractions",
                    tool_name="search_attractions",
                    duration_ms=321.5,
                )
            ],
            evaluations=[
                EvaluationResult(
                    kind="tool_usage",
                    session_id="travel-session-123",
                    span_id="span-123",
                    label="correct",
                    score=1.0,
                    prompt="Plan a day in Chicago",
                )
            ],
        )

    def get_evaluation_summary(self):
        return EvaluationSummary(
            project_name="travel-assistant-assessment",
            total_queries=10,
            tool_usage_incorrect=1,
            frustrated_count=2,
            incorrect_rate=0.1,
            frustration_rate=0.2,
            frustrated_dataset_name="frustrated-demo",
        )

    def get_evaluation_results(self):
        return EvaluationResultsResponse(
            user_frustration=[
                EvaluationResult(
                    kind="user_frustration",
                    session_id="travel-session-1",
                    span_id="span-1",
                    label="frustrated",
                    score=0.0,
                    prompt="Book a hotel",
                )
            ],
            tool_usage=[
                EvaluationResult(
                    kind="tool_usage",
                    session_id="travel-session-2",
                    span_id="span-2",
                    label="incorrect",
                    score=0.0,
                    prompt="Tokyo nightlife",
                    observed_tool_names=["search_web"],
                )
            ],
        )

    def get_frustrated_interactions(self):
        return FrustratedInteractionsResponse(
            items=[
                FrustratedInteraction(
                    session_id="travel-session-1",
                    span_id="span-1",
                    prompt="Book a hotel",
                    response="I cannot do that.",
                    label="frustrated",
                    score=0.0,
                )
            ]
        )

    def get_architecture_content(self):
        return ArchitectureContent(
            mermaid_diagram="flowchart LR\napp --> api\napi --> phoenix",
            runtime_flow=["Runtime Architecture", "Graph Decision Loop"],
            observability_flow=["Observe", "Trace Evidence"],
            evaluation_flow=["Evaluation Pipeline", "User Frustration"],
            production_tradeoffs=["Use stateless replicas", "Keep async eval workers separate"],
            deck_url="http://localhost:4173",
            deck_path="/tmp/presentation/index.html",
        )

    def get_boundary_embeddings(self):
        return BoundaryEmbeddingResponse(
            generated_at="2026-03-20T18:00:00+00:00",
            dataset_name="boundary-prompts-demo",
            embedding_model="text-embedding-3-small",
            dimensions=3,
            summary=BoundaryEmbeddingSummary(
                total_prompts=50,
                worked=41,
                partial=6,
                failed=3,
                success_rate=0.82,
            ),
            points=[
                BoundaryEmbeddingPoint(
                    id=1,
                    prompt="Book me a hotel in Rome.",
                    category="hotel_repeat",
                    expected_behavior="planning_only",
                    response="I cannot book that, but I can help you plan.",
                    session_id="travel-session-boundary-1",
                    success_label="works",
                    success_score=1.0,
                    tool_hints=[],
                    notes=["planning_only"],
                    coords={"x": 0.2, "y": -0.1, "z": 0.5},
                )
            ],
            category_similarity_matrix=[
                BoundaryMatrixRow(
                    row="hotel_repeat",
                    values=[BoundaryMatrixCell(column="hotel_repeat", similarity=0.93)],
                )
            ],
        )

    def get_boundary_projection(self, request):
        return BoundaryProjectionResponse(
            point=BoundaryEmbeddingPoint(
                id=999,
                prompt=request.prompt,
                category="live_prompt",
                expected_behavior="planning_only",
                response=request.response,
                session_id=request.session_id,
                success_label="works",
                success_score=1.0,
                tool_hints=request.tool_hints,
                notes=request.notes,
                source="live",
                expected_refusal=True,
                actual_refusal=True,
                confusion_label="tp",
                coords={"x": 0.15, "y": 0.05, "z": -0.3},
            )
        )


def test_health_endpoint_returns_ok():
    client = TestClient(create_app(agent_executor=FakeAgent()))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_preserves_contract():
    client = TestClient(create_app(agent_executor=FakeAgent()))
    response = client.post("/chat", json={"message": "Plan a day in Chicago"})
    assert response.status_code == 200
    assert response.json() == {"response": "Echo: Plan a day in Chicago"}


def test_chat_ui_endpoint_returns_frontend_shape():
    client = TestClient(create_app(agent_executor=FakeToolAgent()))
    response = client.post("/chat/ui", json={"message": "Plan a day in Chicago"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["response"].startswith("For Plan a day in Chicago")
    assert payload["session_id"].startswith("travel-session-")
    assert payload["tool_hints"] == ["search_attractions"]
    assert payload["sources"] == [{"url": "https://example.com/guide", "label": "Official Guide"}]
    assert "planning" in payload["notes"]


def test_ui_response_marks_planning_only_requests():
    result = {
        "messages": [
            type("Message", (), {"content": "I cannot book that for you, but I can help you plan.", "tool_calls": []})()
        ]
    }
    payload = _build_ui_response(
        prompt="Book me a hotel in Rome",
        session_id="travel-session-test",
        agent_result=result,
    )
    assert payload.notes == ["planning_only"]


def test_demo_overview_returns_ui_safe_summary():
    client = TestClient(create_app(agent_executor=FakeAgent(), demo_service=FakeDemoService()))
    response = client.get("/demo/overview")
    assert response.status_code == 200
    assert response.json()["trace_count"] == 10
    assert response.json()["frustration_rate"] == 0.2


def test_demo_trace_detail_returns_trace_and_span_data():
    client = TestClient(create_app(agent_executor=FakeAgent(), demo_service=FakeDemoService()))
    response = client.get("/demo/traces/trace-123")
    assert response.status_code == 200
    payload = response.json()
    assert payload["trace"]["trace_id"] == "trace-123"
    assert payload["spans"][0]["tool_name"] == "search_attractions"
    assert payload["evaluations"][0]["kind"] == "tool_usage"


def test_demo_evaluation_endpoints_return_results_and_dataset():
    client = TestClient(create_app(agent_executor=FakeAgent(), demo_service=FakeDemoService()))
    summary = client.get("/demo/evaluations/summary")
    results = client.get("/demo/evaluations/results")
    frustrated = client.get("/demo/evaluations/frustrated")
    architecture = client.get("/demo/architecture")

    assert summary.status_code == 200
    assert summary.json()["incorrect_rate"] == 0.1
    assert results.json()["tool_usage"][0]["observed_tool_names"] == ["search_web"]
    assert frustrated.json()["items"][0]["label"] == "frustrated"
    assert "flowchart" in architecture.json()["mermaid_diagram"]


def test_demo_boundary_endpoint_returns_embedding_payload():
    client = TestClient(create_app(agent_executor=FakeAgent(), demo_service=FakeDemoService()))
    response = client.get("/demo/boundaries")
    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total_prompts"] == 50
    assert payload["points"][0]["success_label"] == "works"
    assert payload["category_similarity_matrix"][0]["values"][0]["similarity"] == 0.93


def test_demo_boundary_projection_returns_live_point():
    client = TestClient(create_app(agent_executor=FakeAgent(), demo_service=FakeDemoService()))
    response = client.post(
        "/demo/boundaries/project",
        json={
            "prompt": "Book me a hotel in Rome.",
            "response": "I cannot book that, but I can help you plan it.",
            "session_id": "travel-session-live-1",
            "notes": ["planning_only"],
            "tool_hints": [],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["point"]["source"] == "live"
    assert payload["point"]["confusion_label"] == "tp"
    assert payload["point"]["session_id"] == "travel-session-live-1"
