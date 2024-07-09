import unittest
import asyncio
from fastapi.testclient import TestClient

from core.models.db_helper import test_db_helper
from main import app
from core.models import Base, DatabaseHelper
from core.config import settings
from core.models import db_helper
from tests.apply_migrations import apply_migrations

# Создаем тестовое приложение, используя тот же lifespan
test_app = app

# Переопределяем зависимость get_db для использования тестовой базы данных
test_app.dependency_overrides[db_helper.session_dependency] = (
    test_db_helper.session_dependency
)

client = TestClient(test_app)


class BaseTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    async def asyncSetUpClass(cls):
        apply_migrations()
        await db_helper.create_all()

    @classmethod
    async def asyncTearDownClass(cls):
        await db_helper.drop_all()

    async def asyncSetUp(self):
        async with db_helper.engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())

    async def asyncTearDown(self):
        async with db_helper.engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())