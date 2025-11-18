# app/repositories/user_repositories.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security.hashing import Hash

class UserRepository:
    @staticmethod
    def get_all(db: Session, current_user: models.User):
        if current_user.role == "owner":
            return db.query(models.User).all()

        return db.query(models.User).filter(
            models.User.store_id == current_user.store_id
        ).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(models.User).filter(
            models.User.id == user_id
        ).first()

    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(models.User).filter(
            models.User.username == username
        ).first()

    @staticmethod
    def create(db: Session, user_data: schemas.UserCreate, store_id: int):
        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role=user_data.role or "staff",
            store_id=store_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update(db: Session, user: models.User, updated_data: dict):
        for key, value in updated_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: models.User):
        db.delete(user)
        db.commit()
