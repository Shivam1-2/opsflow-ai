# Development

## Prerequisites

- Docker and Docker Compose
- Optionally Python 3.12+ and Node 22+ for host-side tests/builds

## Start the stack

```bash
docker compose up --build
```

## Seed development users

After migrations, create sample organization and users (development only):

```bash
docker compose exec backend python manage.py seed_dev_data
```

Default password (documented in command output): `dev-password-change-me`

| Email | Role |
|-------|------|
| admin@acme.dev | ADMIN |
| operator@acme.dev | OPERATOR |
| reviewer@acme.dev | REVIEWER |

## Authentication from the frontend

The React app calls `http://localhost:8000` with session cookies. Ensure `VITE_API_BASE_URL=http://localhost:8000` and use the login screen at http://localhost:5173.

Flow:

1. Frontend fetches CSRF cookie (`/api/v1/auth/csrf/`).
2. Login posts credentials to `/api/v1/auth/login/`.
3. Subsequent API calls include cookies and CSRF token.

## Environment variables

See `.env.example`. Do not commit `.env` or production secrets.

## Celery

```bash
docker compose exec backend python manage.py enqueue_health_check
```

## Backend tests

```bash
make backend-test
```

Or with a bind mount for local edits:

```bash
docker compose run --rm --no-deps -v "$PWD/backend:/app" -e RUN_MIGRATIONS=false backend pytest
```

## Frontend build

```bash
make frontend-build
```

## Migrations

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py makemigrations --check --dry-run
```
