# app/schemas/customer.py
from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True
