import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Base
from main import app
from src.users.models import User


@pytest.fixture
async def test_user(session: AsyncSession):
    user = User(
        username="testuser", email="test@example.com", hashed_password="hashed_password"
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
async def session():
    async with db_helper.session_factory() as session:
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
