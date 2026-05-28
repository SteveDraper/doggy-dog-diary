from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Request

from doggy_dog_diary.dogs import (
    create_dog_engine,
    delete_dog_engine,
    get_dog_engine,
    list_dogs_engine,
    update_dog_engine,
)
from doggy_dog_diary.schemas.dog import DogCreate, DogRead, DogUpdate

router = APIRouter(prefix="/api/v1/dogs", tags=["dogs"])


@router.get("", response_model=list[DogRead])
def list_dogs(request: Request) -> list[DogRead]:
    return list_dogs_engine(request.app.state.engine)


@router.post("", response_model=DogRead, status_code=201)
def create_dog(payload: DogCreate, request: Request) -> DogRead:
    return create_dog_engine(request.app.state.engine, payload)


@router.get("/{dog_id}", response_model=DogRead)
def get_dog(dog_id: UUID, request: Request) -> DogRead:
    dog = get_dog_engine(request.app.state.engine, dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@router.patch("/{dog_id}", response_model=DogRead)
def update_dog(dog_id: UUID, payload: DogUpdate, request: Request) -> DogRead:
    dog = update_dog_engine(request.app.state.engine, dog_id, payload)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog


@router.delete("/{dog_id}", status_code=204)
def delete_dog(dog_id: UUID, request: Request) -> None:
    deleted = delete_dog_engine(request.app.state.engine, dog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dog not found")
