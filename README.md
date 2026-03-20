# Travel Assistant Assessment

This repository is now split into three workspaces:

- `backend/`: FastAPI, LangGraph, Phoenix, evaluations, and Docker setup
- `frontend/`: SvelteKit hackathon web app
- `presentation/`: slide deck, architecture notes, and visual source material

## Current Status

- `backend/` serves chat plus Phoenix-backed demo endpoints under `/demo/*`
- `frontend/` is a tabbed app with Chat, Traces, Evaluation, Embeddings, and Architecture views
- `presentation/` remains the source of truth for the deck and production-architecture narrative

## Getting Started

Backend instructions: `backend/README.md`

Frontend instructions: `frontend/README.md`

Typical local demo flow:

1. Start Phoenix from `backend/`
2. Start the FastAPI backend on `localhost:8000`
3. Start the Svelte frontend on `localhost:5173` or `localhost:5174`
4. Use the frontend tabs for chat, traces, evaluation evidence, and architecture context

Presentation assets:

- `presentation/presentation.md`
- `presentation/production_architecture.md`
- `presentation/slides-dist/index.html`
