from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base


if TYPE_CHECKING:
    from src.users.models import User


class Product(Base):

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="products")
