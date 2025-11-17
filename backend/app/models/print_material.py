from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class PrintMaterial(Base):
    __tablename__ = "print_materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # A3, A3+, Banner 260gr
    material_type = Column(String, nullable=False)  # sheet, roll, meter
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    base_unit = Column(String, default="sheet")     # sheet/meter
    purchase_price = Column(Float, default=0)
