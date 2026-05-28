from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from doggy_dog_diary.app import create_app
from doggy_dog_diary.config import AppConfig, ensure_storage_layout, load_config
from doggy_dog_diary.database import create_engine_for_config

BACKEND_DIR = Path(__file__).resolve().parents[1]


def run_migrations(config_path: Path) -> None:
    env = {**__import__("os").environ, "DOGGY_CONFIG": str(config_path)}
    subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(BACKEND_DIR / "alembic.ini"), "upgrade", "head"],
        cwd=BACKEND_DIR,
        check=True,
        env=env,
    )


def make_test_config(tmp_path: Path) -> tuple[AppConfig, Path]:
    storage = tmp_path / "data"
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        yaml.dump(
            {
                "storage_path": str(storage),
                "instance_id": "test-instance",
                "host": "127.0.0.1",
                "port": 8000,
            }
        ),
        encoding="utf-8",
    )
    cfg = load_config(config_file)
    ensure_storage_layout(cfg)
    run_migrations(config_file)
    return cfg, config_file


def make_test_client(tmp_path: Path) -> TestClient:
    cfg, _ = make_test_config(tmp_path)
    engine = create_engine_for_config(cfg)
    return TestClient(create_app(cfg, engine))
