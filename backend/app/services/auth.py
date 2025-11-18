# services/auth.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from repositories.auth_repository import AuthRepository
from schemas.auth import UserCreate, UserOut, TokenData
from models.user import User  # sesuaikan path modelmu

SECRET_KEY = "YOUR_SECRET_KEY"   # nanti bisa pindah ke environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    # -------------------------
    # Utility
    # -------------------------
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def create_access_token(self, data: dict, expires_delta: int = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # -------------------------
    # SIGN UP
    # -------------------------
    async def register_user(self, user_data: UserCreate) -> UserOut:
        # cek email sudah dipakai
        exist = await self.auth_repository.get_user_by_email(user_data.email)
        if exist:
            raise ValueError("Email sudah terdaftar")

        hashed = self.hash_password(user_data.password)
        user_data.password = hashed

        user = await self.auth_repository.create_user(user_data)

        return UserOut(
            id=user.id,
            email=user.email,
            name=user.name,
        )

    # -------------------------
    # LOGIN
    # -------------------------
    async def login(self, email: str, password: str):
        user = await self.auth_repository.get_user_by_email(email)
        if not user:
            raise ValueError("Email tidak ditemukan")

        if not self.verify_password(password, user.password):
            raise ValueError("Password salah")

        token = self.create_access_token({"sub": user.email})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
            },
        }

    # -------------------------
    # VERIFY TOKEN
    # -------------------------
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise JWTError

            return TokenData(email=email)

        except JWTError:
            raise ValueError("Token tidak valid atau kadaluarsa")
