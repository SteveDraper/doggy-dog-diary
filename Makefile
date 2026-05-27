.PHONY: install build frontend run dev dev-api dev-ui test_server test_frontend ci migrate

install:
	uv sync --all-extras
	cd frontend && npm install
	cd frontend && npx playwright install chromium

build: frontend

frontend:
	cd frontend && npm run build

migrate:
	cd backend && uv run alembic upgrade head

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
