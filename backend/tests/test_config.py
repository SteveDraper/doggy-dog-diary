from pathlib import Path

import pytest
import yaml

from doggy_dog_diary.config import ensure_storage_layout, load_config


def test_load_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    storage = tmp_path / "data"
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
    assert cfg.instance_id == "test-instance"
    assert cfg.port == 8000
    assert cfg.database_path == storage.resolve() / "diary.db"


def test_storage_path_relative_to_config_file(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    storage = tmp_path / "nested" / "data"
    config_file.write_text(
        yaml.dump(
            {
                "storage_path": "nested/data",
                "instance_id": "x",
                "host": "127.0.0.1",
                "port": 8000,
            }
        ),
        encoding="utf-8",
    )
    cfg = load_config(config_file)
    assert cfg.storage_path == storage.resolve()


def test_ensure_storage_layout_creates_directories(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    storage = tmp_path / "datadir"
    config_file.write_text(
        yaml.dump(
            {
                "storage_path": str(storage),
                "instance_id": "x",
                "host": "127.0.0.1",
                "port": 8000,
            }
        ),
        encoding="utf-8",
    )
    cfg = load_config(config_file)
    ensure_storage_layout(cfg)
    assert storage.is_dir()
    assert cfg.photos_path.is_dir()
