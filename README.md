# OpsFlow AI

AI-powered operations inbox that transforms unstructured business requests into validated, human-approved business actions.

## Current milestone

**Milestone 2 — Identity, multi-tenancy, requests, and workflow foundation**

Organizations, session authentication, role-based authorization, tenant-isolated text requests, controlled status transitions, audit history, and a minimal React operations UI.

Milestone 1 infrastructure (Docker, Celery, health checks, CI) remains in place.

## Technology stack

- Django + Django REST Framework
- PostgreSQL, Redis, Celery
- React + TypeScript + Vite
- Docker Compose, GitHub Actions

## Local setup

```bash
cp .env.example .env   # optional
docker compose up --build
```

Seed development users (optional):

```bash
docker compose exec backend python manage.py seed_dev_data
```

Password: `dev-password-change-me` (development only — see [Development](docs/development.md)).

## URLs

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health: http://localhost:8000/api/v1/health/

### API (Milestone 2)

| Method | Path |
|--------|------|
| POST | `/api/v1/auth/login/` |
| POST | `/api/v1/auth/logout/` |
| GET | `/api/v1/auth/me/` |
| GET/POST | `/api/v1/requests/` |
| GET | `/api/v1/requests/{id}/` |
| GET | `/api/v1/requests/{id}/status/` |
| GET | `/api/v1/requests/{id}/audit/` |
| POST | `/api/v1/requests/{id}/transitions/` |

## Testing

```bash
make test
```

## Documentation

- [Architecture](docs/architecture.md)
- [Development](docs/development.md)
