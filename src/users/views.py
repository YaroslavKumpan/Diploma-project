from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper
from . import crud
from .schemas import User, UserCreate, UserUpdate, UserUpdatePartial
from .dependencies import user_by_id, check_username, check_email

router = APIRouter(tags=["Users"])


#
@router.get("/", response_model=list[User], operation_id="get_all_users")
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_new_user",
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await check_username(user_in=user_in, session=session)
    await check_email(user_in=user_in, session=session)
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{user_id}/", response_model=User, operation_id="get_user_by_id")
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.put("/{user_id}/", operation_id="update_existing_user")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await check_username(user_in=user_update, session=session)
    await check_email(user_in=user_update, session=session)
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.patch("/{user_id}/", operation_id="partially_update_user")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await check_username(user_in=user_update, session=session)
    await check_email(user_in=user_update, session=session)
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="remove_user",
)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_user(session=session, user=user)
