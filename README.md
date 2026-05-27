# Doggy Dog Diary

Local-first household pet diary. Each device runs an **Instance** (FastAPI + SQLite + SPA).

## Quick start

1. Copy config and set your data directory:

   ```bash
   cp config.example.yaml config.yaml
   ```

2. Install dependencies:

   ```bash
   make install
   ```

3. Run the app (builds the SPA, runs migrations, starts on port 8000):

   ```bash
   make run
   ```

   Or: `uv run doggy-dog-diary start`

4. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the placeholder home screen.

On first start, `storage_path` from config is created (database and `photos/` live there).

## Development

Run API and Vite dev server together (Vite proxies `/api` to the backend):

```bash
make dev
```

Or in two terminals: `make dev-api` and `make dev-ui`. Use [http://127.0.0.1:5173](http://127.0.0.1:5173) during development.

## Layout

| Path | Purpose |
|------|---------|
| `backend/` | FastAPI app, Alembic migrations, built SPA output |
| `frontend/` | TypeScript + Tailwind SPA (Vite) |
| `docs/` | Design docs and ADRs |
| `config.example.yaml` | Sample Instance config |

## Health check

`GET /api/health` — instance id and database connectivity.

## Tests

| Command | What it runs |
|---------|----------------|
| `make test_server` | Backend unit tests (pytest) |
| `make test_frontend` | Frontend tests (Playwright) |
| `make ci` | Both (same as GitHub Actions) |

CI runs on pull requests and pushes to `main` via `.github/workflows/ci.yml`.
