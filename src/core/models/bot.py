from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String, Text

from .base import Base


class Bot(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    price: Mapped[float] = mapped_column(
        Float(precision=2),
        default=None,
        server_default=None,
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    version: Mapped[str] = mapped_column(String(20), unique=False)
    update_description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
