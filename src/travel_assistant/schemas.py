from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="User prompt to send to the agent.")


class ChatResponse(BaseModel):
    response: str


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
