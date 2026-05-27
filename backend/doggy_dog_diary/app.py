from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.engine import Engine

from doggy_dog_diary.config import AppConfig

STATIC_SPA_DIR = Path(__file__).resolve().parent.parent / "static" / "spa"


def create_app(config: AppConfig, engine: Engine) -> FastAPI:
    app = FastAPI(title="Doggy Dog Diary", version="0.1.0")
    app.state.config = config
    app.state.engine = engine

    @app.get("/api/health")
    def health() -> dict[str, str | bool]:
        db_ok = False
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            db_ok = True
        except Exception:
            db_ok = False
        return {
            "status": "ok" if db_ok else "degraded",
            "instance_id": config.instance_id,
            "database": db_ok,
        }

    if STATIC_SPA_DIR.is_dir() and (STATIC_SPA_DIR / "index.html").is_file():
        assets_dir = STATIC_SPA_DIR / "assets"
        if assets_dir.is_dir():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="spa-assets")

        @app.get("/{full_path:path}")
        def spa_fallback(full_path: str) -> FileResponse:
            # API routes are registered above; this catches client-side routes.
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="Not found")
            file_path = STATIC_SPA_DIR / full_path
            if full_path and file_path.is_file():
                return FileResponse(file_path)
            return FileResponse(STATIC_SPA_DIR / "index.html")

    return app
