from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Определяем базовый каталог
BASE_DIR = Path(__file__).parent.parent

# Загружаем переменные окружения из .env файла
load_dotenv()


class Settings(BaseSettings):
    db_url: str
    test_db_url: str
    db_echo: bool

    class Config:
        env_file = ".env"


# Создаём экземпляр настроек
settings = Settings()

# Формируем полный путь в коде
settings.db_url = settings.db_url.replace("///", f"///{BASE_DIR}/")
settings.test_db_url = settings.test_db_url.replace("///", f"///{BASE_DIR}/")
