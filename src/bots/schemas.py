from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String, Text


class BotBase(BaseModel):
    title: str
    price: float
    body: Text
    version: Text
    bot_link: str


class BotCreate(BotBase):
    pass


class Bot(BotBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
