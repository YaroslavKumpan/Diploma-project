from typing import Annotated

from fastapi import APIRouter, Path

from src.users import crud
from src.users.schemas import CreateUser

router = APIRouter(prefix="/users")


@router.post("/create_user/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)


@router.get("/{user_id}")
def get_user_id_from_db(user_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "user_id": user_id,
    }
