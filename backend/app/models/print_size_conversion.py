from sqlalchemy import Column, ForeignKey, Integer, String, Float
from app.db.database import Base

class PrintSizeConversion(Base):
    __tablename__ = "print_size_conversion"

    id = Column(Integer, primary_key=True)
    from_material_id = Column(Integer, ForeignKey("print_materials.id"))
    to_size_name = Column(String, nullable=False)
    fit_count = Column(Integer, nullable=False)
    waste_percentage = Column(Float, default=0)
