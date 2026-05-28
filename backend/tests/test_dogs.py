from pathlib import Path

from tests.conftest import make_test_client


def test_list_dogs_empty(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    response = client.get("/api/v1/dogs")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_dog(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    payload = {
        "name": "Nico",
        "date_of_birth": "2019-03-15",
        "sex": "male",
        "breed": "Labrador",
        "neutered": True,
        "microchip": "985112004567890",
        "status": "current",
        "description": "Anxious around loud noises.",
        "kc_registered_name": "Ch Example Nico",
        "kc_number": "KC123456",
        "kc_body": "The Kennel Club",
    }
    create = client.post("/api/v1/dogs", json=payload)
    assert create.status_code == 201
    body = create.json()
    assert body["name"] == "Nico"
    assert body["date_of_birth"] == "2019-03-15"
    assert body["sex"] == "male"
    assert body["breed"] == "Labrador"
    assert body["neutered"] is True
    assert body["microchip"] == "985112004567890"
    assert body["status"] == "current"
    assert body["description"] == "Anxious around loud noises."
    assert body["kc_registered_name"] == "Ch Example Nico"
    assert body["kc_number"] == "KC123456"
    assert body["kc_body"] == "The Kennel Club"
    assert body["profile_photo_path"] is None

    dog_id = body["id"]
    get = client.get(f"/api/v1/dogs/{dog_id}")
    assert get.status_code == 200
    assert get.json()["name"] == "Nico"


def test_update_dog(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    create = client.post("/api/v1/dogs", json={"name": "Bella"})
    dog_id = create.json()["id"]

    patch = client.patch(
        f"/api/v1/dogs/{dog_id}",
        json={
            "description": "Loves fetch.",
            "status": "rehomed",
            "status_date": "2025-01-10",
            "kc_number": "KC999",
        },
    )
    assert patch.status_code == 200
    body = patch.json()
    assert body["description"] == "Loves fetch."
    assert body["status"] == "rehomed"
    assert body["status_date"] == "2025-01-10"
    assert body["kc_number"] == "KC999"


def test_list_dogs_sorts_current_first(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    client.post("/api/v1/dogs", json={"name": "Zara", "status": "deceased"})
    client.post("/api/v1/dogs", json={"name": "Bella", "status": "current"})
    client.post("/api/v1/dogs", json={"name": "Nico", "status": "current"})

    response = client.get("/api/v1/dogs")
    names = [dog["name"] for dog in response.json()]
    assert names == ["Bella", "Nico", "Zara"]


def test_delete_dog(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    create = client.post("/api/v1/dogs", json={"name": "Temp"})
    dog_id = create.json()["id"]

    delete = client.delete(f"/api/v1/dogs/{dog_id}")
    assert delete.status_code == 204
    assert client.get(f"/api/v1/dogs/{dog_id}").status_code == 404


def test_get_missing_dog_returns_404(tmp_path: Path) -> None:
    client = make_test_client(tmp_path)
    response = client.get("/api/v1/dogs/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 404
