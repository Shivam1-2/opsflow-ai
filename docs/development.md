# Development

## Prerequisites

- Docker and Docker Compose
- Optionally Python 3.12+ and Node 22+ for running tests/builds on the host

## Start the stack

```bash
docker compose up --build
```

Useful Make targets:

```bash
make up
make down
make build
make logs
make test
make backend-test
make frontend-build
```

## Environment variables

See `.env.example`. Docker Compose interpolates a local `.env` file when present and otherwise uses the documented defaults.

Do not commit `.env`. Never put real secrets in the repository.

## Frontend API URL

The browser calls Django directly, so `VITE_API_BASE_URL` should be a host-reachable URL such as `http://localhost:8000`. Development CORS allows `http://localhost:5173`. CSRF is not disabled.

## Celery

Redis is the Celery broker. The worker command is:

```bash
celery -A config worker --loglevel=info
```

Enqueue the foundation test task against a running stack:

```bash
docker compose exec backend python manage.py enqueue_health_check
```

The worker log should show `health_check_task` completing. Unit tests call the task eagerly and do not require a live worker.

## Backend tests on the host

```bash
cd backend
pip install -r requirements/development.txt
pytest
```

`pytest.ini` selects `config.settings.test`.

## Frontend build on the host

```bash
cd frontend
npm ci
npm run build
```

## Production settings

`config.settings.production` is a structure for later deployment. It refuses to start with `DEBUG` enabled or with the placeholder secret key. It is not a complete production deployment.
