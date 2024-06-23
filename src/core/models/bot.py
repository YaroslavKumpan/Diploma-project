from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String, Text, DateTime

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
    bot_link: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=None,
    )
    version: Mapped[str] = mapped_column(String(20), unique=False)
    update_description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=None,
    )
