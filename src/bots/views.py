from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import db_helper
from . import crud
from .dependencies import bot_by_id
from .schemas import Bot, BotCreate


router = APIRouter(tags=["Bots"], prefix="/bots")


@router.get(
    "/",
    response_model=list[Bot],
)
async def get_bots(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_bots(session=session)


@router.post(
    "/",
    response_model=Bot,
    status_code=status.HTTP_201_CREATED,
)
async def create_bot(
    bot_in: BotCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_bot(session=session, bot_in=bot_in)


@router.get(
    "/{bot_id}/",
    response_model=Bot,
)
async def get_bot(bot=Depends(bot_by_id)):
    return bot
