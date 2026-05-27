from pathlib import Path

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from doggy_dog_diary import app as app_module
from doggy_dog_diary.app import create_app, resolve_static_spa_path
from doggy_dog_diary.config import AppConfig
from doggy_dog_diary.database import create_engine_for_config


def test_resolve_static_spa_path_rejects_parent_traversal(tmp_path: Path) -> None:
    static_root = tmp_path / "spa"
    static_root.mkdir()
    (static_root / "index.html").write_text("ok", encoding="utf-8")
    secret = tmp_path / "secret.txt"
    secret.write_text("secret", encoding="utf-8")

    with pytest.raises(HTTPException) as exc:
        resolve_static_spa_path("../secret.txt", static_root=static_root)
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException):
        resolve_static_spa_path("assets/../../secret.txt", static_root=static_root)


def test_resolve_static_spa_path_allows_file_under_root(tmp_path: Path) -> None:
    static_root = tmp_path / "spa"
    assets = static_root / "assets"
    assets.mkdir(parents=True)
    bundle = assets / "app.js"
    bundle.write_text("console.log(1)", encoding="utf-8")

    resolved = resolve_static_spa_path("assets/app.js", static_root=static_root)
    assert resolved == bundle.resolve()


def test_spa_fallback_blocks_traversal_requests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    static_root = tmp_path / "spa"
    static_root.mkdir()
    (static_root / "index.html").write_text("<html></html>", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")

    monkeypatch.setattr(app_module, "STATIC_SPA_DIR", static_root)

    storage = tmp_path / ".data"
    storage.mkdir()
    config = AppConfig(
        storage_path=storage,
        instance_id="test",
        host="127.0.0.1",
        port=8000,
    )
    engine = create_engine_for_config(config)
    client = TestClient(create_app(config, engine))

    # Starlette may normalize literal ".." segments before routing; encoded segments reach us.
    for path in (
        "/%2e%2e%2f%2e%2e%2foutside.txt",
        "/%2e%2e/outside.txt",
        "/assets/%2e%2e%2f%2e%2e%2foutside.txt",
    ):
        response = client.get(path)
        assert response.status_code == 404, path
        assert "outside" not in response.text

    spa_route = client.get("/dogs/1")
    assert spa_route.status_code == 200
    assert "text/html" in spa_route.headers.get("content-type", "")
