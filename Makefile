.PHONY: install build frontend run dev dev-api dev-ui test_server test_frontend ci migrate

REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ifneq (,$(wildcard $(REPO_ROOT)/config.yaml))
  CONFIG_PATH := $(REPO_ROOT)/config.yaml
else ifneq (,$(wildcard $(REPO_ROOT)/config.local.yaml))
  CONFIG_PATH := $(REPO_ROOT)/config.local.yaml
endif

install:
	uv sync --all-extras
	cd frontend && npm install
	cd frontend && npx playwright install chromium

build: frontend

frontend:
	cd frontend && npm run build

migrate:
ifndef CONFIG_PATH
	$(error No config.yaml found. Copy config.example.yaml to config.yaml at the repo root.)
endif
	cd backend && DOGGY_CONFIG="$(CONFIG_PATH)" uv run alembic upgrade head

run: build
	uv run doggy-dog-diary start

dev-api:
	uv run doggy-dog-diary start

dev-ui:
	cd frontend && npm run dev

dev:
	@echo "API http://127.0.0.1:8000 · SPA dev http://127.0.0.1:5173 (proxies /api)"
	@trap 'kill 0' INT; \
		uv run doggy-dog-diary start & \
		cd frontend && npm run dev; \
		wait

test_server:
	uv run pytest

test_frontend:
	cd frontend && npm run test

ci: test_server test_frontend
