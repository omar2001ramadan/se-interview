FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/backend

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY backend/pyproject.toml backend/poetry.lock backend/README.md ./
COPY backend/src ./src
COPY backend/artifacts ./artifacts
COPY backend/evals ./evals
COPY backend/api.py backend/agent.py ./
COPY presentation /app/presentation

RUN poetry install --only main --no-interaction --no-ansi

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
