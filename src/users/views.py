from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper
from . import crud
from .dependencies import user_by_id
from .schemas import UserCreate, User, UserUpdate, UserUpdatePartial

router = APIRouter(tags=["Users"])


@router.get("/",
            response_model=list[User],
            operation_id="list_users")
async def get_users(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_users(session=session)


@router.post("/",
             response_model=User,
             status_code=status.HTTP_201_CREATED,
             operation_id="create_user")
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.create_user(
        session=session,
        user_in=user_in)


@router.get("/{user_id}/",
            response_model=User,
            operation_id="get_user")
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.put("/{user_id}/", operation_id="update_user")
async def update_user(
        user_update: UserUpdate,
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update)


@router.patch("/{user_id}/", operation_id="partial_update_user")
async def update_user_partial(
        user_update: UserUpdatePartial,
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True)


@router.delete("/{user_id}/",
               status_code=status.HTTP_204_NO_CONTENT,
               operation_id="delete_user")
async def delete_user(
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> None:
    await crud.delete_user(
        session=session,
        user=user)
