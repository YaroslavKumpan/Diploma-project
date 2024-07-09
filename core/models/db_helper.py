from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from core.config import settings


# Класс помощник для работы с базой данных
class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # Используется для того, чтобы одна и та же сессия могла быть использована в рамках одной асинхронной задачи.
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    # создание сессии каждый раз, при новом обращении в views инициализируем новую сессию
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    # или когда мы работаем с одной scoped session
    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()


# Инициализация основной базы данных
db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
# Инициализация тестовой бд
test_db_helper = DatabaseHelper(
    url=settings.test_db_url,
    echo=settings.db_echo,
)
