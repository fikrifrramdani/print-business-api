# app/schemas/product_schemas.py
from pydantic import BaseModel
from typing import Optional

# ===== CATEGORY =====
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        orm_mode = True


# ===== PRODUCT =====
class ProductBase(BaseModel):
    code: str
    name: str
    type: str  # barang / jasa
    cost_price: float
    sell_price: float
    stock: Optional[int] = 0
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    cost_price: Optional[float] = None
    sell_price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    profit: float
    profit_percent: float

    class Config:
        orm_mode = True
