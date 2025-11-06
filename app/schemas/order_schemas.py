# app/schemas/order_schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ✅ Item di dalam order
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    price_at_order: float  # harga saat transaksi

    class Config:
        orm_mode = True


# ✅ Order utama
class OrderBase(BaseModel):
    customer_name: str
    total_amount: float

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    total_amount: Optional[float] = None

class OrderResponse(OrderBase):
    id: int
    store_id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        orm_mode = True
