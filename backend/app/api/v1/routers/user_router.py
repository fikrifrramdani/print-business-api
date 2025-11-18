#app/api/v1/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.models.user import User
from app.utils.deps import get_db
from app.core.security.auth_utils import get_current_user
from app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserRepository.get_all(db, current_user)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if current_user.role == "admin" and user.store_id != current_user.store_id:
        raise HTTPException(403, "Access denied")

    return user


@router.post("/", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check username
    if UserRepository.get_by_username(db, data.username):
        raise HTTPException(400, "Username already exists")

    # determine store
    if current_user.role == "owner":
        if not data.store_id:
            raise HTTPException(400, "Owner must specify store_id")
        store_id = data.store_id
    else:
        store_id = current_user.store_id

    return UserRepository.create(db, data, store_id)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if current_user.role == "admin" and user.store_id != current_user.store_id:
        raise HTTPException(403, "Access denied")

    update_data = data.dict(exclude_unset=True, exclude={"password"})
    
    # handle password
    if data.password:
        update_data["hashed_password"] = hash_password(data.password)

    return UserRepository.update(db, user, update_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if current_user.role == "admin" and user.store_id != current_user.store_id:
        raise HTTPException(403, "Access denied")

    UserRepository.delete(db, user)
