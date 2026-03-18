from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from travel_assistant.config import get_settings
from travel_assistant.graph import build_agent
from travel_assistant.observability import configure_observability, maybe_using_attributes
from travel_assistant.query_loader import session_id_for_prompt
from travel_assistant.schemas import ChatRequest, ChatResponse

load_dotenv()


def create_app(agent_executor=None) -> FastAPI:
    settings = get_settings()
    configure_observability(settings)

    app = FastAPI(
        title="Travel Assistant Agent API",
        description="Travel planning assistant backed by LangGraph, DuckDuckGo, and Arize Phoenix",
        version="0.2.0",
    )
    app.state.agent = agent_executor
    app.state.settings = settings

    @app.post("/chat", response_model=ChatResponse)
    def chat(request: ChatRequest) -> ChatResponse:
        session_id = session_id_for_prompt(request.message)
        if app.state.agent is None:
            app.state.agent = build_agent(app.state.settings)
        with maybe_using_attributes(
            session_id=session_id,
            metadata={"route": "/chat", "project": settings.phoenix_project_name},
        ):
            result = app.state.agent.invoke({"messages": [HumanMessage(content=request.message)]})
        return ChatResponse(response=result["messages"][-1].content)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
