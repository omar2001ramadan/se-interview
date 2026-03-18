# Travel Assistant Assessment

Travel assistant assessment project built on FastAPI, LangGraph, DuckDuckGo-backed tools, and Arize Phoenix.

## What Changed

- Refactored the starter into a package under `src/travel_assistant/`
- Added a new structured LangGraph tool: `search_attractions(destination, interests, max_results)`
- Kept a DuckDuckGo-backed fallback tool for fresh current-information lookups
- Added Phoenix tracing hooks, query corpus scripts, tests, Docker assets, and presentation material

## Prerequisites

- Python 3.11 to 3.13
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker Desktop or Docker Engine
- OpenAI API key

## Setup

1. Install dependencies:

```bash
poetry install
```

2. Create an environment file:

```bash
cp .env.example .env
```

3. Populate `.env`:

```bash
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4o
OPENAI_EVAL_MODEL=gpt-4o-mini
TRACING_ENABLED=true
PHOENIX_PROJECT_NAME=travel-assistant-assessment
PHOENIX_BASE_URL=http://localhost:6006
PHOENIX_COLLECTOR_ENDPOINT=http://localhost:6006/v1/traces
```

## Run Phoenix

Start the Phoenix UI and collector locally:

```bash
docker compose up phoenix -d
```

Phoenix will be available at [http://localhost:6006](http://localhost:6006).

## Run the API

```bash
poetry run uvicorn api:app --reload
```

The API listens on [http://localhost:8000](http://localhost:8000).

## API Contract

`POST /chat`

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have one day in Chicago and love architecture. What should I do?"}'
```

`GET /health`

```bash
curl http://localhost:8000/health
```

## Run Tests

```bash
poetry run pytest
```

## Run The 10-Query Trace Experiment

1. Start Phoenix.
2. Start the API.
3. Run the seeded corpus:

```bash
poetry run python scripts/run_queries.py
```

Responses will be saved to `artifacts/query_runs.json`.

## Export Spans And Run Evaluations

```bash
poetry run python scripts/export_and_evaluate.py
```

Current outputs:

- `artifacts/spans.json`
- `artifacts/spans.csv`
- `artifacts/root_spans.json`
- `artifacts/tool_usage_evaluations.json`
- `artifacts/user_frustration_evaluations.json`
- `artifacts/frustrated_interactions.json`
- `artifacts/evaluation_summary.json`

The export script also logs `tool_usage_correctness` and `user_frustration` annotations back to Phoenix and creates a dataset of frustrated interactions when any are detected.

## Docker

Run both the application and Phoenix:

```bash
docker compose up --build
```

## Project Layout

```text
.
├── api.py
├── agent.py
├── artifacts/
├── docs/
├── evals/
├── scripts/
├── src/travel_assistant/
├── tests/
├── Dockerfile
└── docker-compose.yml
```

## Observability Notes

- Phoenix OTEL registration happens during app startup in `src/travel_assistant/api.py`
- LangChain/OpenInference instrumentation is configured in `src/travel_assistant/observability.py`
- Each `/chat` request is wrapped with session metadata so traces are easier to inspect in Phoenix

## Architecture And Presentation Assets

- Production architecture: `docs/production_architecture.md`
- Design decisions: `docs/design_decisions.md`
- Presentation outline: `docs/presentation.md`
- Reveal.js interview deck: `docs/slides/index.html`

## Present The Deck Locally

Serve the slide directory with a simple local web server:

```bash
cd docs/slides
python3 -m http.server 4173
```

Then open [http://localhost:4173](http://localhost:4173).

Presenter tips:

- Press `S` to open speaker notes in a second window.
- Use the slide number and progress bar for pacing.
- The deck is built as a local-first reveal.js site with vendored reveal assets, so it does not depend on a CDN during the interview.
