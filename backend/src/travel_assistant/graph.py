from __future__ import annotations

import operator
from typing import Annotated, Literal

from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from travel_assistant.config import Settings, get_settings
from travel_assistant.tools import build_tools, serialize_tool_output


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


SYSTEM_PROMPT = """You are a travel assistant powered by tools.

Use `search_attractions` when the user is asking what to do in a destination, asking for sights,
activities, neighborhoods, museums, parks, restaurants, or trip-planning suggestions. That tool
returns structured attraction results and should be your first choice for travel planning.

Use `search_web` when the user asks for current or time-sensitive information such as news, events,
weather, regulations, airline updates, opening hours, or anything else that may have changed.

You cannot book flights, hotels, or tickets. If a user asks you to transact or reserve something,
be explicit that you cannot complete the booking and offer planning guidance instead.

When a tool returns JSON, read it carefully, cite the most relevant source URLs in your response,
and summarize rather than dumping raw JSON back to the user.
"""


def build_agent(settings: Settings | None = None):
    settings = settings or get_settings()
    tools = build_tools()
    tools_by_name = {tool.name: tool for tool in tools}

    model = ChatOpenAI(model=settings.openai_model, temperature=settings.openai_temperature)
    model_with_tools = model.bind_tools(tools)

    def llm_call(state: MessagesState) -> dict:
        return {
            "messages": [
                model_with_tools.invoke(
                    [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
                )
            ]
        }

    def tool_node(state: MessagesState) -> dict:
        result = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append(
                ToolMessage(
                    content=serialize_tool_output(observation),
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": result}

    def should_continue(state: MessagesState) -> Literal["tool_node", "__end__"]:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tool_node"
        return END

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("llm_call", llm_call)
    graph_builder.add_node("tool_node", tool_node)
    graph_builder.add_edge(START, "llm_call")
    graph_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    graph_builder.add_edge("tool_node", "llm_call")
    return graph_builder.compile()
