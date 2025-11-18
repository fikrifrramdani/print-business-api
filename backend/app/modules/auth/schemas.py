# app/modules/auth/schemas.py
from pydantic import BaseModel
from typing import Optional


# === Register ===
class RegisterRequest(BaseModel):
    username: str
    password: str


# === Login (form-data tetap dipakai via OAuth2PasswordRequestForm) ===
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str
    store_id: int
    store_name: str


# === User (yang dikembalikan dari auth) ===
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    store_id: int

    class Config:
        orm_mode = True
