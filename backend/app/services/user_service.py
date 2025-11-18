# app/services/user_service.py
from fastapi import HTTPException, status
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user

    async def create_user(self, data):
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(400, "Email already registered")
        return await self.repo.create(data)

    async def update_user(self, user_id: int, data):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        return await self.repo.update(user, data)

    async def delete_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        await self.repo.delete(user)
        return {"message": "User deleted"}
