# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.models.user import User
from app.models.store import Store
from app.core.security.auth_utils import hash_password, verify_password, create_access_token, get_current_user
from app.schemas.user_schemas import UserCreate
from app.core.security.hashing import Hash
from app.schemas.user_schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Register user baru ---
@router.post("/register")
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    # Cek apakah username sudah dipakai
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash password
    hashed_password = Hash.bcrypt(request.password)

    # === 1️⃣ Buat store lebih dulu ===
    store_name = f"Toko {request.username.capitalize()}"
    new_store = Store(name=store_name)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)

    # === 2️⃣ Buat user dan link ke store ===
    new_user = User(
        username=request.username,
        hashed_password=hashed_password,
        role="owner",
        store_id=new_store.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # === 3️⃣ Update store owner_id ===
    new_store.owner_id = new_user.id
    db.commit()

    return {
        "message": "User & store created successfully",
        "username": new_user.username,
        "store_name": new_store.name,
        "store_id": new_store.id
    }

# --- Login user ---
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username atau password salah")

    # buat token JWT
    token = create_access_token({
        "sub": user.username,
        "user_id": user.id,
        "role": user.role,
        "store_id": user.store_id
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
        "store_id": user.store_id,
        "store_name": user.store.name
    }

# --- Endpoint test ---
@router.get("/test")
def test_auth():
    return {"message": "Auth router aktif"}

# --- GET: List semua user dalam 1 toko (hanya owner) ---
@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Pastikan hanya owner yang bisa akses
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Hanya owner yang dapat melihat data user")

    # Ambil semua user berdasarkan store_id
    users = db.query(User).filter(User.store_id == current_user.store_id).all()

    if not users:
        raise HTTPException(status_code=404, detail="Belum ada user di toko ini")

    return users