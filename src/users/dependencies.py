from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate, UserUpdatePartial
from . import crud

"""
user_by_id используется получения пользователя по айди, если пользователь не найде в БД, то райзится ошибка 404.
"""


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found",
    )


# Проверка на существование пользователя с таким же username
async def check_username(
    user_in: UserCreate | UserUpdate | UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    stmt = select(User).where(User.username == user_in.username)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=422, detail="Username already registered")


# Проверка на существование пользователя с таким же email
async def check_email(
    user_in: UserCreate | UserUpdate | UserUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    stmt = select(User).where(User.email == user_in.email)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=422, detail="Email already registered")
