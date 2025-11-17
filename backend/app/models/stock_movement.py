from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class StockMovement(Base):
    __tablename__ = "stock_movement"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    material_id = Column(Integer, ForeignKey("print_materials.id"), nullable=True)
    movement_type = Column(String)  # in/out/production
    quantity = Column(Float)
    ref_id = Column(Integer, nullable=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
