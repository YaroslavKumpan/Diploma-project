from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper
from . import crud
from .schemas import User, UserCreate
from .dependencies import user_by_id, check_username, check_email

router = APIRouter(tags=["Users"])


# получение списка пользователей
@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


# создание нового пользователя
@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    _check_username_dependency: None = Depends(check_username),
    _check_email_dependency: None = Depends(check_email),
):
    return await crud.create_user(session=session, user_in=user_in)


# получение пользователя по айди
@router.get("/{user_id}/", response_model=User)
async def get_user(user: User = Depends(user_by_id)):
    return user
