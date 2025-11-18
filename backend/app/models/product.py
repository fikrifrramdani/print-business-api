# app/models/product.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String)  # jasa / barang
    cost_price = Column(Float, default=0.0)
    sell_price = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    profit_percent = Column(Float, default=0.0)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("product_categories.id"))

    category = relationship("ProductCategory", back_populates="products")
    stock_movements = relationship("StockMovement", back_populates="product")