# routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import UserCreate, UserOut
from services.auth import AuthService
from repositories.auth_repository import AuthRepository
from database import get_db  # sesuaikan dengan path DB session kamu (SQLAlchemy async)

router = APIRouter(prefix="/auth", tags=["Auth"])


# Dependency injection untuk service
def get_auth_service(db=Depends(get_db)):
    repo = AuthRepository(db)
    return AuthService(repo)


# ----------------------------------------
# REGISTER
# ----------------------------------------
@router.post("/register", response_model=UserOut)
async def register_user(
    user_data: UserCreate, 
    service: AuthService = Depends(get_auth_service)
):
    try:
        return await service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


# ----------------------------------------
# LOGIN
# ----------------------------------------
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):
    try:
        return await service.login(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
