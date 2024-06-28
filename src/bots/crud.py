from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models import Bot
from sqlalchemy.engine import Result
from .schemas import Bot, BotCreate


async def get_bots(session: AsyncSession) -> list[Bot]:
    stmt = select(Bot).order_by(Bot.id)
    result: Result = await session.execute(stmt)
    bots = result.scalars().all()
    return list(bots)


async def get_bot(session: AsyncSession, bot_id: int) -> Bot | None:
    return await session.get(Bot, bot_id)


async def create_bot(
    session: AsyncSession,
    bot_in: BotCreate,
) -> Bot:
    bot = Bot(**bot_in.model_dump())
    session.add(bot)
    await session.commit()
    await session.refresh(bot)
    return bot


async def delete_bot(session: AsyncSession, bot: Bot) -> None:
    await session.delete(bot)
    await session.commit()
