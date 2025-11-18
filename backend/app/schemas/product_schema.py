# app/schemas/product_schema.py
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
    name: Optional[str]
    category: Optional[str]
    description: Optional[str]
    price: Optional[float]


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
