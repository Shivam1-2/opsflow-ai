# OpsFlow AI

AI-powered operations inbox that transforms unstructured business requests into validated, human-approved business actions.

This project is currently under development.

## Current milestone

**Milestone 1 — Project Foundation**

This milestone provides the local development stack only: Django, Django REST Framework, PostgreSQL, Redis, Celery, and a React + TypeScript frontend. Application domain features are not implemented yet.

## Technology stack

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- React
- TypeScript
- Docker

## Local setup

Copy environment defaults if you want a local override (optional — Compose already uses `.env.example` values):

```bash
cp .env.example .env
```

Start the full stack:

```bash
docker compose up --build
```

Or:

```bash
make up
```

## URLs

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health: http://localhost:8000/api/v1/health/
- Readiness: http://localhost:8000/api/v1/health/ready/

## Testing

Backend tests (SQLite + eager Celery, no running worker required):

```bash
make backend-test
```

Frontend production build:

```bash
make frontend-build
```

Run both:

```bash
make test
```

From the backend directory without Docker:

```bash
pip install -r requirements/development.txt
pytest
```

From the frontend directory without Docker:

```bash
npm ci
npm run build
```

To confirm Django → Redis → Celery worker against the running stack:

```bash
docker compose exec backend python manage.py enqueue_health_check
```

## Documentation

- [Architecture](docs/architecture.md)
- [Development](docs/development.md)
