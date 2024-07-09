from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    user_id: int


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductBase):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
