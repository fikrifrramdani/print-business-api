from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from app.db.database import Base

class InvoiceRetail(Base):
    __tablename__ = "invoice_retail"

    id = Column(Integer, primary_key=True)
    cashier_id = Column(Integer, ForeignKey("users.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0)
