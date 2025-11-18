# app/routers/store_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.store import Store
from app.schemas.store_schemas import StoreCreate, StoreUpdate, StoreResponse
from typing import List

router = APIRouter(prefix="/stores", tags=["Stores"])

# --- Ambil semua toko ---
@router.get("/", response_model=List[StoreResponse])
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()

# --- Tambah toko baru ---
@router.post("/", response_model=StoreResponse)
def add_store(data: StoreCreate, db: Session = Depends(get_db)):
    existing = db.query(Store).filter(Store.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Toko '{data.name}' sudah ada")

    store = Store(
        name=data.name,
        address=data.address,
        phone=data.phone,
        owner=data.owner
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

# --- Update toko ---
@router.put("/{store_id}", response_model=StoreResponse)
def update_store(store_id: int, data: StoreUpdate, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Toko tidak ditemukan")

    store.name = data.name
    store.address = data.address
    store.phone = data.phone
    store.owner = data.owner

    db.commit()
    db.refresh(store)
    return store

# --- Hapus toko ---
@router.delete("/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Toko tidak ditemukan")

    db.delete(store)
    db.commit()
    return {"message": "Toko dihapus"}
