from sqlalchemy.orm import Mapped

from core.models.base import Base


class Product(Base):
    ___tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
