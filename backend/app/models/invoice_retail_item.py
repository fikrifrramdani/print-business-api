from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class InvoiceRetailItem(Base):
    __tablename__ = "invoice_retail_items"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoice_retail.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)
    subtotal = Column(Float)
