from pathlib import Path

from tests.conftest import make_test_client


def test_health_endpoint(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["instance_id"] == "test-instance"
    assert body["database"] is True
