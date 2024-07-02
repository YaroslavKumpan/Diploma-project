from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from .base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="products")
