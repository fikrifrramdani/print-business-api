# app/routes/user.py
from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserOut, UserUpdate
from services.user_service import UserService
from repositories.user_repository import UserRepository
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db=Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return await service.get_user(user_id)


@router.post("/", response_model=UserOut)
async def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(data)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return await service.update_user(user_id, data)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.delete_user(user_id)
