from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from doggy_dog_diary.config import AppConfig


def database_url(db_path: Path) -> str:
    return f"sqlite:///{db_path}"


def create_engine_for_config(config: AppConfig) -> Engine:
    return create_engine(
        database_url(config.database_path),
        connect_args={"check_same_thread": False},
    )


def check_connection(engine: Engine) -> bool:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
