from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from doggy_dog_diary.app import create_app
from doggy_dog_diary.config import ensure_storage_layout, load_config
from doggy_dog_diary.database import create_engine_for_config


def _client(tmp_path: Path) -> TestClient:
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
    engine = create_engine_for_config(cfg)
    return TestClient(create_app(cfg, engine))


def test_health_endpoint(tmp_path: Path) -> None:
    client = _client(tmp_path)
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["instance_id"] == "test-instance"
    assert body["database"] is True
