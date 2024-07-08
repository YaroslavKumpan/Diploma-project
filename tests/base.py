import unittest
import asyncio
from fastapi.testclient import TestClient
from main import app
from core.models import Base, DatabaseHelper
from core.config import settings
from core.models import db_helper


# Переопределяем db_helper для использования тестовой базы данных
test_db_helper = DatabaseHelper(
    url=settings.test_db_url,
    echo=settings.db_echo,
)

# Создаем тестовое приложение, используя тот же lifespan
test_app = app

# Переопределяем зависимость get_db для использования тестовой базы данных
test_app.dependency_overrides[db_helper.session_dependency] = (
    test_db_helper.session_dependency
)

client = TestClient(test_app)


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создание всех таблиц в тестовой базе данных
        async def async_setUpClass():
            async with test_db_helper.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        asyncio.run(async_setUpClass())

    @classmethod
    def tearDownClass(cls):
        # Удаление всех таблиц в тестовой базе данных
        async def async_tearDownClass():
            async with test_db_helper.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        asyncio.run(async_tearDownClass())

    def setUp(self):
        # Очистка базы данных перед каждым тестом
        async def async_setUp():
            async with test_db_helper.engine.begin() as conn:
                for table in reversed(Base.metadata.sorted_tables):
                    await conn.execute(table.delete())

        asyncio.run(async_setUp())
