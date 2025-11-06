# app/models/order.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    order_number = Column(String, unique=True)
    order_date = Column(Date)
    customer_name = Column(String)
    status = Column(String, default="Design")
    store_id = Column(Integer, ForeignKey("stores.id"))

    store = relationship("Store", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
