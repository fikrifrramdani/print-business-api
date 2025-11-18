# app/models/store.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    owner = Column(String, nullable=True)

    # ✅ Tambahkan ini untuk relasi ke Order
    orders = relationship("Order", back_populates="store")

    # 🔧 Tambahkan relasi ini ke User
    users = relationship("User", back_populates="store")