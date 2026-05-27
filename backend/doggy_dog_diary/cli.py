from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import uvicorn

from doggy_dog_diary.app import create_app
from doggy_dog_diary.config import ensure_storage_layout, find_config_path, load_config
from doggy_dog_diary.database import check_connection, create_engine_for_config


def _run_migrations(explicit_config: str | None) -> None:
    backend_dir = Path(__file__).resolve().parent.parent
    alembic_ini = backend_dir / "alembic.ini"
    if not alembic_ini.is_file():
        return
    resolved = (
        Path(explicit_config).expanduser().resolve()
        if explicit_config
        else find_config_path()
    )
    env = {**__import__("os").environ, "DOGGY_CONFIG": str(resolved)}
    subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(alembic_ini), "upgrade", "head"],
        cwd=backend_dir,
        check=True,
        env=env,
    )


def start(config: str | None = None, skip_migrate: bool = False) -> None:
    cfg = load_config(config)
    ensure_storage_layout(cfg)
    if not skip_migrate:
        _run_migrations(config)
    engine = create_engine_for_config(cfg)
    check_connection(engine)
    app = create_app(cfg, engine)
    uvicorn.run(app, host=cfg.host, port=cfg.port, log_level="info")


def main() -> None:
    parser = argparse.ArgumentParser(prog="doggy-dog-diary")
    sub = parser.add_subparsers(dest="command", required=True)

    start_parser = sub.add_parser("start", help="Run the Instance (API + built SPA)")
    start_parser.add_argument(
        "--config",
        "-c",
        help="Path to config YAML (default: config.yaml in cwd)",
    )
    start_parser.add_argument(
        "--skip-migrate",
        action="store_true",
        help="Skip Alembic migrations (for tests)",
    )

    args = parser.parse_args()
    if args.command == "start":
        start(config=args.config, skip_migrate=args.skip_migrate)


if __name__ == "__main__":
    main()
