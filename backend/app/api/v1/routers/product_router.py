# app/api/v1/routers/product_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.modules.product.repository import ProductRepository
from app.modules.product.service import ProductService
from app.modules.product.schemas import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return ProductService(repo)

@router.get("/", response_model=List[ProductOut])
def list_products(service: ProductService = Depends(get_product_service)):
    return service.list_products()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    return service.get_product(product_id)

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.create_product(payload)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, service: ProductService = Depends(get_product_service)):
    return service.update_product(product_id, payload)

@router.delete("/{product_id}")
def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    return service.delete_product(product_id)
