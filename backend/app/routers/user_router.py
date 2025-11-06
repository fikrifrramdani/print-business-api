from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils.auth_utils import get_current_user, hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ✅ Get all users (owner bisa semua, admin hanya cabangnya)
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == "owner":
        users = db.query(models.User).all()
    elif current_user.role == "admin":
        users = db.query(models.User).filter(models.User.store_id == current_user.store_id).all()
    else:
        raise HTTPException(status_code=403, detail="Access denied")
    return users


# ✅ Get single user
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # admin hanya boleh lihat user di cabangnya
    if current_user.role == "admin" and user.store_id != current_user.store_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return user

# ✅ Create user (owner bisa tentukan cabang, admin otomatis cabang sendiri)
@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Cek username unik
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Tentukan store
    if current_user.role == "owner":
        if not user.store_id:
            raise HTTPException(status_code=400, detail="Owner must specify store_id for new user")
        store_id = user.store_id
    elif current_user.role == "admin":
        store_id = current_user.store_id
    else:
        raise HTTPException(status_code=403, detail="Access denied")

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role or "staff",
        store_id=store_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ✅ Update user
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    updated_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # admin hanya boleh ubah user di cabangnya
    if current_user.role == "admin" and user.store_id != current_user.store_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Update password jika ada
    if updated_data.password:
        user.hashed_password = hash_password(updated_data.password)

    # Update field lain
    for key, value in updated_data.dict(exclude={"password"}, exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# ✅ Delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role == "admin" and user.store_id != current_user.store_id:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(user)
    db.commit()
    return None
