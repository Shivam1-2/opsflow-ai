# Contributing to OpsFlow AI

Thank you for your interest in contributing. This document explains how to work on the project locally and what we expect in pull requests.

## Before you start

- Read [README.md](README.md) and [docs/development.md](docs/development.md).
- Do not commit secrets (`.env`, API keys, passwords). Use `.env.example` for documented defaults only.
- Milestone scope is intentional: avoid adding AI, billing, or integrations unless they are part of the agreed roadmap.

## Development setup

```bash
docker compose up --build
```

Run tests before opening a PR:

```bash
make test
```

Backend only:

```bash
make backend-test
```

Frontend build:

```bash
make frontend-build
```

## Branch and commit guidelines

- Use short, descriptive branch names (for example `fix/tenant-isolation`, `feat/request-filter`).
- Write commit messages in the imperative mood (for example `Add request status endpoint`).
- Do not include internal planning labels (such as "week 1") in commit messages.
- One logical change per commit when possible.

## Pull requests

- Keep PRs focused and reasonably sized.
- Ensure CI passes (backend pytest, frontend lint and build).
- Describe **what** changed and **why**.
- Add or update tests for behavior changes.
- Update documentation when APIs, setup, or architecture change.

## Code style

- **Python:** Follow existing Django/DRF patterns in `backend/`. Match surrounding naming and structure.
- **TypeScript/React:** Follow existing patterns in `frontend/`. Run `npm run lint` in the frontend directory.
- Prefer minimal, readable diffs over large refactors unrelated to the task.

## Security and tenancy

- Enforce authorization and organization scoping on the **backend**. Never rely on the frontend alone.
- Do not accept client-supplied `organization`, `created_by`, or arbitrary `status` values on request APIs.

## Questions

Open a GitHub issue using the appropriate template, or contact the maintainers via the process in [SECURITY.md](SECURITY.md) for sensitive topics.
