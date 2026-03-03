# Architecture

OpsFlow AI will eventually receive unstructured business requests, convert them into structured data, validate them, apply business rules, route them through human approval, execute controlled actions, and keep an audit trail.

Milestone 1 implements only the runtime foundation:

```
Browser
  ↓
React + TypeScript + Vite
  ↓ HTTP
Django + Django REST Framework
  ├── PostgreSQL
  └── Redis
        ↓
      Celery
        ↓
      Celery Worker
```

## Services

| Service   | Role |
|-----------|------|
| `frontend` | Vite development server for the React UI |
| `backend`  | Django + DRF API (`/api/v1/`) |
| `worker`   | Celery worker subscribed to Redis |
| `postgres` | Application database |
| `redis`    | Celery broker (and result backend) |

PostgreSQL and Redis are not published to the host. The browser talks to Django on `localhost:8000` and to Vite on `localhost:5173`.

## API versioning

All HTTP APIs are mounted under `/api/v1/`. Core endpoints live in `apps.core`; later domains should add their own apps and URL modules instead of expanding `config/urls.py`.

Current endpoints:

- `GET /api/v1/health/` — liveness
- `GET /api/v1/health/ready/` — PostgreSQL and Redis connectivity

## Settings

Django settings are split:

- `config.settings.base` — shared configuration
- `config.settings.development` — local Docker / laptop
- `config.settings.production` — restrictive production scaffold (`DEBUG` is always false)
- `config.settings.test` — pytest (SQLite, eager Celery)

Environment-specific values come from environment variables. Secrets are not hard-coded.

## Out of scope for this milestone

Organization, application users, roles, authentication, domain models, workflows, AI providers, and third-party integrations are intentionally absent.
