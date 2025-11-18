# app/api/v1/routers/customer_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.modules.customer.repository import CustomerRepository
from app.modules.customer.service import CustomerService
from app.modules.customer.schemas import CustomerCreate, CustomerUpdate, CustomerOut

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_customer_service(db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    return CustomerService(repo)

@router.get("/", response_model=List[CustomerOut])
def list_customers(service: CustomerService = Depends(get_customer_service)):
    return service.list_customers()

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, service: CustomerService = Depends(get_customer_service)):
    return service.get_customer(customer_id)

@router.post("/", response_model=CustomerOut)
def create_customer(payload: CustomerCreate, service: CustomerService = Depends(get_customer_service)):
    return service.create_customer(payload)

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, payload: CustomerUpdate, service: CustomerService = Depends(get_customer_service)):
    return service.update_customer(customer_id, payload)

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, service: CustomerService = Depends(get_customer_service)):
    return service.delete_customer(customer_id)
