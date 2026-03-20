# Railway Deployment

This repo can now be split into three Railway services:

- `backend`: FastAPI API
- `frontend`: public website
- `slides`: reveal.js slide deck

## Service Config Files

Railway config-as-code supports custom file locations. Set each service's config file path in Railway to:

- backend: `/backend/railway.json`
- frontend: `/frontend/railway.json`
- slides: `/presentation/slides-src/railway.json`

These paths are absolute within the repository, matching Railway's current config-as-code docs.

## Recommended Service Setup

Create three services from the same repo:

1. `backend`
2. `frontend`
3. `slides`

Each service should use its matching custom `railway.json` file above. The Dockerfile path and watch patterns are already defined there.

## Required Variables

### Backend

- `OPENAI_API_KEY`: required
- `OPENAI_MODEL`: optional, defaults to `gpt-4o`
- `OPENAI_EVAL_MODEL`: optional, defaults to `gpt-4o-mini`
- `TRACING_ENABLED`: optional
- `PHOENIX_PROJECT_NAME`: optional
- `PHOENIX_BASE_URL`: optional unless you have a reachable Phoenix deployment
- `PHOENIX_COLLECTOR_ENDPOINT`: optional unless you have a reachable Phoenix deployment
- `CORS_ALLOWED_ORIGINS`: set this to the website public URL, for example `https://your-website.up.railway.app`
- `PRESENTATION_DECK_URL`: set this to the slides public URL, for example `https://your-slides.up.railway.app`

### Frontend

- `PUBLIC_API_BASE_URL`: set this to the backend public URL, for example `https://your-backend.up.railway.app`

### Slides

- no required variables

## Notes

- The backend image now includes `backend/artifacts`, `backend/evals`, and the top-level `presentation/` directory so the demo endpoints still work in Railway.
- The backend now reads allowed browser origins from `CORS_ALLOWED_ORIGINS` instead of being locked to localhost.
- The backend now reads the public slide-deck link from `PRESENTATION_DECK_URL` instead of hardcoding `http://localhost:4173`.
- The frontend now builds as a static SvelteKit site and is served with Caddy on Railway's assigned `PORT`.
- The slides deck is built and served independently from the website.
