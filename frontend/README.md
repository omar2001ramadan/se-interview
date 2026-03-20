# Frontend

SvelteKit web app for the travel assistant.

The frontend reuses the visual language from `../presentation/` and exposes four tabs:

- `Chat`
- `Traces`
- `Evaluation`
- `Embeddings`
- `Architecture`

## Setup

```bash
cd frontend
npm install
cp .env.example .env
```

## Run

```bash
npm run dev
```

The app will call the backend using `PUBLIC_API_BASE_URL`.

Expected backend services:

- FastAPI on `http://localhost:8000`
- Phoenix on `http://localhost:6006`

The browser talks only to FastAPI. The backend proxies Phoenix trace data and serves evaluation and architecture content through `/demo/*`.

The `Embeddings` tab reads the backend's boundary-testing artifact and renders a 3D prompt projection plus a category similarity matrix.
