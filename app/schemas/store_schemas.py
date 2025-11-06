# app/schemas/store_schemas.py
from pydantic import BaseModel
from typing import Optional

class StoreBase(BaseModel):
    name: str
    address: str | None = None
    phone: str | None = None
    owner: str | None = None

class StoreCreate(StoreBase):
    pass

class StoreUpdate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int

    class Config:
        orm_mode = True
