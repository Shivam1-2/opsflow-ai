# Architecture

OpsFlow AI transforms unstructured business requests into structured, validated, human-approved actions. Milestone 2 adds identity, multi-tenancy, the request domain, controlled lifecycle transitions, and audit foundations.

## Runtime stack

```
Browser (React + Vite)
  ↓ session cookie + CSRF
Django + Django REST Framework (/api/v1/)
  ├── PostgreSQL (organizations, users, requests, audit)
  └── Redis → Celery worker
```

## Domain model

```
Organization
  ├── User (ADMIN | OPERATOR | REVIEWER)
  └── Request
        └── AuditLog (append-only)
```

Each user belongs to exactly one organization. Requests are owned by an organization and created by a user. Audit entries record request creation and controlled status changes.

## Services

| Service   | Role |
|-----------|------|
| `frontend` | React UI (login, requests) |
| `backend`  | Django + DRF API |
| `worker`   | Celery (Milestone 1 health task; future async work) |
| `postgres` | Primary database |
| `redis`    | Celery broker |

## Authentication

The browser uses **Django session authentication**:

- `GET /api/v1/auth/csrf/` sets the CSRF cookie.
- `POST /api/v1/auth/login/` establishes the session.
- Authenticated API calls send cookies (`credentials: 'include'`) and CSRF on mutating requests.

Protected APIs require authentication. Health endpoints remain public.

## Authorization and tenant isolation

Authorization is enforced in Django REST Framework permission classes. Request querysets are always scoped to `request.user.organization`. Cross-tenant object access returns **404** so UUIDs cannot be probed across tenants.

Roles:

| Role | Capabilities (Milestone 2) |
|------|----------------------------|
| ADMIN | View org requests; perform allowed workflow transitions |
| OPERATOR | Create requests; view org requests; `RECEIVED → PROCESSING` |
| REVIEWER | View org requests (review actions come later) |

## Request lifecycle

Statuses model the future workflow (`RECEIVED` through `COMPLETED`). Milestone 2 does **not** run AI, validation, approval, or action execution. New requests start at `RECEIVED`.

Clients cannot PATCH `status`. Changes go through `POST /api/v1/requests/{id}/transitions/` and `RequestWorkflowService`, which validates transitions, uses transactions with row locks, and writes audit events.

## Audit

`AuditLog` records append-only events such as `REQUEST_CREATED` and `STATUS_CHANGED`. There is no public API to modify audit rows.

## API layout

- `apps.core` — health/readiness
- `apps.accounts` — auth (`/api/v1/auth/`)
- `apps.requests` — requests (`/api/v1/requests/`)
- `apps.organizations` — organization model (no public CRUD in M2)
- `apps.audit` — audit model and serializers

## Settings

- `config.settings.base` — shared configuration
- `config.settings.development` — CORS with credentials for Vite
- `config.settings.test` — SQLite, eager Celery
- `config.settings.production` — scaffold (no DEBUG)

## Out of scope (Milestone 2)

AI/LLM processing, document upload, validation engines, reviewer approval/rejection, action execution, notifications, and external integrations are intentionally not implemented.
