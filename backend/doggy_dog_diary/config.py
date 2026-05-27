from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG_FILENAMES = ("config.yaml", "config.local.yaml")


@dataclass(frozen=True)
class AppConfig:
    storage_path: Path
    instance_id: str
    host: str
    port: int

    @property
    def database_path(self) -> Path:
        return self.storage_path / "diary.db"

    @property
    def photos_path(self) -> Path:
        return self.storage_path / "photos"


def _expand_path(value: str, *, base_dir: Path | None = None) -> Path:
    expanded = Path(os.path.expanduser(value))
    if expanded.is_absolute():
        return expanded.resolve()
    root = (base_dir or Path.cwd()).resolve()
    return (root / expanded).resolve()


def _config_search_roots() -> list[Path]:
    """Walk cwd and parents so config at the repo root is found from backend/."""
    seen: set[Path] = set()
    roots: list[Path] = []
    for directory in (Path.cwd(), *Path.cwd().parents):
        resolved = directory.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        roots.append(resolved)
    return roots


def find_config_path(explicit: str | None = None) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {path}")
        return path

    for directory in _config_search_roots():
        for name in DEFAULT_CONFIG_FILENAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate.resolve()

    raise FileNotFoundError(
        "No config.yaml found. Copy config.example.yaml to config.yaml at the project root "
        "and edit storage_path."
    )


def load_config(config_path: str | Path | None = None) -> AppConfig:
    path = find_config_path(str(config_path) if config_path else None)
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    required = ("storage_path", "instance_id", "host", "port")
    missing = [key for key in required if key not in raw]
    if missing:
        raise ValueError(f"Config missing required keys: {', '.join(missing)}")

    return AppConfig(
        storage_path=_expand_path(str(raw["storage_path"]), base_dir=path.parent),
        instance_id=str(raw["instance_id"]),
        host=str(raw["host"]),
        port=int(raw["port"]),
    )


def ensure_storage_layout(config: AppConfig) -> None:
    """Create data directory and photos folder on first run."""
    config.storage_path.mkdir(parents=True, exist_ok=True)
    config.photos_path.mkdir(parents=True, exist_ok=True)
