from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine

from doggy_dog_diary.schemas.dog import DogCreate, DogRead, DogSex, DogStatus, DogUpdate

_DOG_COLUMNS = """
    id, name, date_of_birth, sex, breed, neutered, microchip,
    status, status_date,
    kc_registered_name, kc_number, kc_body,
    description, profile_photo_path,
    created_at, updated_at
"""

_LIST_ORDER = """
    ORDER BY
        CASE WHEN status = 'current' THEN 0 ELSE 1 END,
        name COLLATE NOCASE
"""


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _date_to_str(value: date | None) -> str | None:
    return value.isoformat() if value is not None else None


def _str_to_date(value: str | None) -> date | None:
    if value is None:
        return None
    return date.fromisoformat(value)


def _bool_to_int(value: bool | None) -> int | None:
    if value is None:
        return None
    return 1 if value else 0


def _int_to_bool(value: int | None) -> bool | None:
    if value is None:
        return None
    return bool(value)


def _parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _row_to_dog(row: Any) -> DogRead:
    mapping = row._mapping
    return DogRead(
        id=UUID(mapping["id"]),
        name=mapping["name"],
        date_of_birth=_str_to_date(mapping["date_of_birth"]),
        sex=DogSex(mapping["sex"]),
        breed=mapping["breed"],
        neutered=_int_to_bool(mapping["neutered"]),
        microchip=mapping["microchip"],
        status=DogStatus(mapping["status"]),
        status_date=_str_to_date(mapping["status_date"]),
        kc_registered_name=mapping["kc_registered_name"],
        kc_number=mapping["kc_number"],
        kc_body=mapping["kc_body"],
        description=mapping["description"],
        profile_photo_path=mapping["profile_photo_path"],
        created_at=_parse_datetime(mapping["created_at"]),
        updated_at=_parse_datetime(mapping["updated_at"]),
    )


def list_dogs(conn: Connection) -> list[DogRead]:
    result = conn.execute(
        text(f"SELECT {_DOG_COLUMNS} FROM dogs {_LIST_ORDER}")
    )
    return [_row_to_dog(row) for row in result]


def get_dog(conn: Connection, dog_id: UUID) -> DogRead | None:
    result = conn.execute(
        text(f"SELECT {_DOG_COLUMNS} FROM dogs WHERE id = :id"),
        {"id": str(dog_id)},
    )
    row = result.first()
    return _row_to_dog(row) if row else None


def create_dog(conn: Connection, payload: DogCreate) -> DogRead:
    now = _utc_now()
    dog_id = uuid4()
    conn.execute(
        text(
            f"""
            INSERT INTO dogs ({_DOG_COLUMNS})
            VALUES (
                :id, :name, :date_of_birth, :sex, :breed, :neutered, :microchip,
                :status, :status_date,
                :kc_registered_name, :kc_number, :kc_body,
                :description, :profile_photo_path,
                :created_at, :updated_at
            )
            """
        ),
        {
            "id": str(dog_id),
            "name": payload.name,
            "date_of_birth": _date_to_str(payload.date_of_birth),
            "sex": payload.sex.value,
            "breed": payload.breed,
            "neutered": _bool_to_int(payload.neutered),
            "microchip": payload.microchip,
            "status": payload.status.value,
            "status_date": _date_to_str(payload.status_date),
            "kc_registered_name": payload.kc_registered_name,
            "kc_number": payload.kc_number,
            "kc_body": payload.kc_body,
            "description": payload.description,
            "profile_photo_path": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        },
    )
    dog = get_dog(conn, dog_id)
    assert dog is not None
    return dog


def update_dog(conn: Connection, dog_id: UUID, payload: DogUpdate) -> DogRead | None:
    existing = get_dog(conn, dog_id)
    if existing is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return existing

    field_map = {
        "name": "name",
        "date_of_birth": "date_of_birth",
        "sex": "sex",
        "breed": "breed",
        "neutered": "neutered",
        "microchip": "microchip",
        "status": "status",
        "status_date": "status_date",
        "kc_registered_name": "kc_registered_name",
        "kc_number": "kc_number",
        "kc_body": "kc_body",
        "description": "description",
    }

    set_clauses: list[str] = []
    params: dict[str, Any] = {"id": str(dog_id)}

    for key, column in field_map.items():
        if key not in updates:
            continue
        value = updates[key]
        if key == "date_of_birth" or key == "status_date":
            value = _date_to_str(value)
        elif key == "sex" or key == "status":
            value = value.value if value is not None else None
        elif key == "neutered":
            value = _bool_to_int(value)
        set_clauses.append(f"{column} = :{column}")
        params[column] = value

    set_clauses.append("updated_at = :updated_at")
    params["updated_at"] = _utc_now().isoformat()

    conn.execute(
        text(f"UPDATE dogs SET {', '.join(set_clauses)} WHERE id = :id"),
        params,
    )
    return get_dog(conn, dog_id)


def delete_dog(conn: Connection, dog_id: UUID) -> bool:
    result = conn.execute(
        text("DELETE FROM dogs WHERE id = :id"),
        {"id": str(dog_id)},
    )
    return result.rowcount > 0


def list_dogs_engine(engine: Engine) -> list[DogRead]:
    with engine.connect() as conn:
        return list_dogs(conn)


def get_dog_engine(engine: Engine, dog_id: UUID) -> DogRead | None:
    with engine.connect() as conn:
        return get_dog(conn, dog_id)


def create_dog_engine(engine: Engine, payload: DogCreate) -> DogRead:
    with engine.begin() as conn:
        return create_dog(conn, payload)


def update_dog_engine(engine: Engine, dog_id: UUID, payload: DogUpdate) -> DogRead | None:
    with engine.begin() as conn:
        return update_dog(conn, dog_id, payload)


def delete_dog_engine(engine: Engine, dog_id: UUID) -> bool:
    with engine.begin() as conn:
        return delete_dog(conn, dog_id)
