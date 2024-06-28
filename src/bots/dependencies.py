from typing import Annotated

from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from src.core.models import db_helper, Bot


async def bot_by_id(
    bot_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Bot:
    bot = await crud.get_bot(session=session, bot_id=bot_id)
    if bot is not None:
        return bot

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Bot {bot_id} not found!"
    )
