# app/modules/auth/repository.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.store import Store
from app.core.security.password import Hash


class AuthRepository:

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_store(db: Session, store_name: str) -> Store:
        new_store = Store(name=store_name)
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        return new_store

    @staticmethod
    def create_owner_user(db: Session, username: str, password: str, store_id: int) -> User:
        hashed_password = Hash.bcrypt(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            role="owner",
            store_id=store_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_store_owner(db: Session, store: Store, owner_id: int):
        store.owner_id = owner_id
        db.commit()

    @staticmethod
    def get_users_by_store(db: Session, store_id: int):
        return db.query(User).filter(User.store_id == store_id).all()
