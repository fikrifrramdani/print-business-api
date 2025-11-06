# app/main.py
import warnings
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app import models
from app.routers import (
    auth_router,
    product_router,
    order_router,
    finance_router,
    store_router,
    user_router
)
from app.seeders.finance_seeder import seed_finance_data
from app.seeders.owner_seeder import seed_owner_if_empty  # ✅ tambahkan ini
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Print Business Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nanti bisa dibatasi ke domain FE kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Buat tabel otomatis
Base.metadata.create_all(bind=engine)

# ✅ Seeder otomatis jalan saat startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_finance_data(db)
    seed_owner_if_empty(db)
    db.close()

# ✅ Register semua router
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(finance_router.router)
app.include_router(store_router.router)

# ✅ Endpoint root
@app.get("/")
def root():
    return {"message": "API is running"}
