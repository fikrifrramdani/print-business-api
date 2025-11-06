# # app/models/finance.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class FinanceCategory(Base):
    __tablename__ = "finance_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # income / expense / saving

    records = relationship("FinanceRecord", back_populates="category")


class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("finance_categories.id"))
    amount = Column(Float)
    note = Column(String)
    date = Column(Date)
    period = Column(String)  # ex: "Nov-25"
    source = Column(String)  # ex: "Business Income"

    category = relationship("FinanceCategory", back_populates="records")
