from __future__ import annotations

import json
import re
from typing import Any

from ddgs import DDGS
from langchain_core.tools import tool

from travel_assistant.schemas import (
    AttractionResult,
    AttractionSearchInput,
    AttractionSearchOutput,
    SearchResult,
    WebSearchInput,
    WebSearchOutput,
)

TITLE_SPLIT_RE = re.compile(r"\s+[|\-:]\s+")
CATEGORY_KEYWORDS = {
    "museum": "museum",
    "gallery": "art",
    "art": "art",
    "park": "park",
    "garden": "park",
    "trail": "outdoors",
    "beach": "beach",
    "nightlife": "nightlife",
    "bar": "nightlife",
    "restaurant": "food",
    "food": "food",
    "historic": "historic site",
    "history": "historic site",
    "market": "shopping",
    "shopping": "shopping",
    "zoo": "family",
    "aquarium": "family",
    "theme park": "family",
    "viewpoint": "landmark",
    "tower": "landmark",
    "cathedral": "landmark",
}
PAID_KEYWORDS = {
    "ticket",
    "admission",
    "museum",
    "tour",
    "cruise",
    "aquarium",
    "zoo",
    "theme park",
}
FREE_KEYWORDS = {
    "park",
    "garden",
    "beach",
    "walking",
    "riverwalk",
    "promenade",
    "neighborhood",
    "market",
    "viewpoint",
}


def _perform_search(
    query: str,
    *,
    max_results: int,
    region: str = "wt-wt",
    search_client_cls: type[DDGS] = DDGS,
) -> list[dict[str, Any]]:
    with search_client_cls() as search_client:
        results = search_client.text(
            query,
            region=region,
            safesearch="moderate",
            max_results=max_results,
        )
        return list(results)


def _clean_title(title: str) -> str:
    parts = TITLE_SPLIT_RE.split(title)
    return parts[0].strip() if parts else title.strip()


def _clip(text: str, limit: int = 220) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else f"{text[: limit - 3].rstrip()}..."


def _infer_category(text: str) -> str:
    lowered = text.lower()
    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in lowered:
            return category
    return "general attraction"


def _infer_cost(text: str, category: str) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in PAID_KEYWORDS):
        return "Paid or ticketed"
    if category in {"park", "beach", "landmark"} or any(keyword in lowered for keyword in FREE_KEYWORDS):
        return "Usually free"
    return "Varies"


def _build_rationale(destination: str, interests: list[str], category: str, snippet: str) -> str:
    lowered = snippet.lower()
    for interest in interests:
        interest_clean = interest.strip()
        if interest_clean and interest_clean.lower() in lowered:
            return f"Matches the stated interest in {interest_clean} around {destination}."
    if interests:
        joined = ", ".join(interests[:3])
        return f"Relevant to {destination} travel planning and aligned with interests like {joined}."
    return f"Representative {category} option surfaced for {destination}."


def normalize_attraction_results(
    search_input: AttractionSearchInput,
    raw_results: list[dict[str, Any]],
) -> AttractionSearchOutput:
    attractions: list[AttractionResult] = []
    notes: list[str] = []
    seen_urls: set[str] = set()
    if not raw_results:
        notes.append("No attraction results were returned from DuckDuckGo.")

    for raw_result in raw_results:
        url = raw_result.get("href") or raw_result.get("url") or ""
        title = raw_result.get("title") or raw_result.get("name") or "Unknown attraction"
        snippet = raw_result.get("body") or raw_result.get("snippet") or ""
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        cleaned_title = _clean_title(title)
        category = _infer_category(f"{cleaned_title} {snippet}")
        attractions.append(
            AttractionResult(
                name=cleaned_title,
                category=category,
                summary=_clip(snippet or f"Popular stop in {search_input.destination}."),
                estimated_cost=_infer_cost(f"{cleaned_title} {snippet}", category),
                rationale=_build_rationale(
                    search_input.destination,
                    search_input.interests,
                    category,
                    f"{cleaned_title} {snippet}",
                ),
                source_url=url,
            )
        )
        if len(attractions) >= search_input.max_results:
            break

    if attractions:
        notes.append("Results are normalized from live DuckDuckGo web search snippets.")
    return AttractionSearchOutput(
        destination=search_input.destination,
        attractions=attractions,
        notes=notes,
    )


def _normalize_web_results(query: str, raw_results: list[dict[str, Any]], max_results: int) -> WebSearchOutput:
    results: list[SearchResult] = []
    seen_urls: set[str] = set()
    for raw_result in raw_results:
        url = raw_result.get("href") or raw_result.get("url") or ""
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        title = raw_result.get("title") or raw_result.get("name") or "Untitled result"
        snippet = raw_result.get("body") or raw_result.get("snippet") or ""
        results.append(
            SearchResult(
                title=_clean_title(title),
                snippet=_clip(snippet or "No summary available."),
                source_url=url,
            )
        )
        if len(results) >= max_results:
            break
    return WebSearchOutput(query=query, results=results)


@tool(args_schema=WebSearchInput)
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web with DuckDuckGo for fresh facts, news, and changing information."""
    raw_results = _perform_search(query, max_results=max_results)
    return _normalize_web_results(query, raw_results, max_results).model_dump_json(indent=2)


@tool(args_schema=AttractionSearchInput)
def search_attractions(destination: str, interests: list[str], max_results: int = 5) -> str:
    """Find destination attractions with structured output for travel planning."""
    search_input = AttractionSearchInput(
        destination=destination,
        interests=interests,
        max_results=max_results,
    )
    interest_text = ", ".join(search_input.interests) if search_input.interests else "top sights"
    query = f"best attractions in {search_input.destination} for {interest_text}"
    raw_results = _perform_search(query, max_results=max_results * 2)
    return normalize_attraction_results(search_input, raw_results).model_dump_json(indent=2)


def serialize_tool_output(observation: Any) -> str:
    if isinstance(observation, str):
        return observation
    if hasattr(observation, "model_dump_json"):
        return observation.model_dump_json(indent=2)
    return json.dumps(observation, indent=2, default=str)


def build_tools() -> list[Any]:
    return [search_attractions, search_web]
