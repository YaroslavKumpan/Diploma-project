from datetime import datetime
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: Annotated[str, MinLen(8), MaxLen(40)]


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    hashed_password: Annotated[str, MinLen(8), MaxLen(40)]
