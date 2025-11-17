from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class InvoicePrint(Base):
    __tablename__ = "invoice_print"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer")
    order_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, default=0)
    payment_status = Column(String, default="unpaid")
