from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DogSex(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class DogStatus(str, Enum):
    current = "current"
    deceased = "deceased"
    rehomed = "rehomed"


class DogBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    date_of_birth: date | None = None
    sex: DogSex = DogSex.unknown
    breed: str | None = None
    neutered: bool | None = None
    microchip: str | None = None
    status: DogStatus = DogStatus.current
    status_date: date | None = None
    kc_registered_name: str | None = None
    kc_number: str | None = None
    kc_body: str | None = None
    description: str | None = None


class DogCreate(DogBase):
    pass


class DogUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    date_of_birth: date | None = None
    sex: DogSex | None = None
    breed: str | None = None
    neutered: bool | None = None
    microchip: str | None = None
    status: DogStatus | None = None
    status_date: date | None = None
    kc_registered_name: str | None = None
    kc_number: str | None = None
    kc_body: str | None = None
    description: str | None = None


class DogRead(DogBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    profile_photo_path: str | None = None
    created_at: datetime
    updated_at: datetime
