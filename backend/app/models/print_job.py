from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.db.database import Base

class PrintJob(Base):
    __tablename__ = "print_jobs"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoice_print.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    material_id = Column(Integer, ForeignKey("print_materials.id"))
    size_name = Column(String)
    quantity = Column(Integer)
    width = Column(Float)
    height = Column(Float)
    total_material_used = Column(Float)
    status = Column(String, default="waiting")
