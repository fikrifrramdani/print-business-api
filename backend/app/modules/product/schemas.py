# app/modules/product/schemas.py
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
