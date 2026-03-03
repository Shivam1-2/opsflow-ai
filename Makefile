.PHONY: up down build logs test backend-test frontend-build

COMPOSE ?= docker compose

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f

test: backend-test frontend-build

backend-test:
	$(COMPOSE) run --rm --no-deps -e RUN_MIGRATIONS=false backend pytest

frontend-build:
	$(COMPOSE) run --rm --no-deps frontend npm run build
