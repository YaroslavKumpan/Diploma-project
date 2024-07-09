import unittest

from fastapi.testclient import TestClient

from core.models import Base
from core.models import db_helper
from core.models.db_helper import test_db_helper
from main import app
from tests.apply_migrations import apply_migrations

# Создаем тестовое приложение, используя тот же lifespan
test_app = app

# Переопределяем зависимость db_helper для использования тестовой базы данных
test_app.dependency_overrides[db_helper.session_dependency] = (
    test_db_helper.session_dependency
)

client = TestClient(test_app)


# Базовый класс тестов для асинхронных тестов
class BaseTest(unittest.IsolatedAsyncioTestCase):

    @classmethod
    async def asyncSetUpClass(cls):
        # Применяем миграции и создаем все таблицы в тестовой базе данных
        apply_migrations()
        await db_helper.create_all()

    @classmethod
    async def asyncTearDownClass(cls):
        # Удаляем все таблицы из тестовой базы данных
        await db_helper.drop_all()

    async def asyncSetUp(self):
        # Очищаем все таблицы перед каждым тестом
        async with db_helper.engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())

    async def asyncTearDown(self):
        # Очищаем все таблицы после каждого теста
        async with db_helper.engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())
