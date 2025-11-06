# app/schemas/user_schemas.py
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str | None = None
    store_id: int | None = None
    role: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
