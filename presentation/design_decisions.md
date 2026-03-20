# Design Decisions

## Why `search_attractions`

- The assessment requires at least one additional tool that integrates into the agent workflow and returns structured output.
- Attractions fit the travel-assistant scenario without introducing paid booking APIs or credentials for third-party providers.
- A structured attractions tool is easier to evaluate than a purely free-form search tool because it has a stable schema.

## Why Keep Generic Web Search

- The starter project already handled current-information lookups with web search.
- Travel assistants still need a fresh-information path for weather, advisories, flight delays, and changing policies.
- Separating `search_attractions` from `search_web` makes tool routing observable and testable.

## Why `tool_usage_correctness` As The Custom Metric

- It directly measures whether the agent chooses the right tool for the user’s intent.
- It is easy to explain during the interview using traces and tool spans.
- It complements user-frustration scoring by focusing on agent behavior rather than only final user sentiment.

## Why Phoenix In Docker

- Docker is the fastest reproducible local setup for an interview environment.
- It also aligns with the repository deliverable requirement to include Docker configuration.

## Why A Scripted 10-Query Corpus

- The assessment explicitly requires at least 10 traces.
- A fixed corpus gives deterministic demo inputs across planning, current-information, and unsupported-booking scenarios.
- Including unsupported booking prompts creates realistic frustrated interactions for the Phoenix evaluation workflow.
