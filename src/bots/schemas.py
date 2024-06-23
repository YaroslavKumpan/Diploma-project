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
        from_attributes=True
    )
    id: int


# class BotBase(BaseModel):
#     title: Mapped[str] = mapped_column(String(100), unique=False)
#     price: Mapped[float] = mapped_column(
#         Float(precision=2),
#         default=None,
#         server_default=None,
#     )
#     body: Mapped[str] = mapped_column(
#         Text,
#         default="",
#         server_default="",
#     )
#     version: Mapped[str] = mapped_column(String(20), unique=False)
#     update_description: Mapped[str] = mapped_column(
#         Text,
#         default="",
#         server_default="",
#     )


# class BotUpdate(BotBase):
#     pass
#
#
# class BotUpdatePartial(BotBase):
#     name: str | None = None
#     price: int | None = None
#     description: str | None = None
#
#
# class BotDelete(BotBase):
#     model_config = ConfigDict(
#         from_attributes=True
#     )  # чтобы возвразался на резульатат с БД, а json
#     id: int
