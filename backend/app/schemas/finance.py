from pydantic import BaseModel
from datetime import date

# ============================
#  Category
# ============================

class FinanceCategoryBase(BaseModel):
    name: str
    type: str  # income / expense / saving

class FinanceCategoryCreate(FinanceCategoryBase):
    pass

class FinanceCategoryResponse(FinanceCategoryBase):
    id: int
    class Config:
        orm_mode = True


# ============================
#  Record
# ============================

class FinanceRecordBase(BaseModel):
    category_id: int
    amount: float
    note: str | None = None
    date: date
    period: str
    source: str

class FinanceRecordCreate(FinanceRecordBase):
    pass

class FinanceRecordResponse(FinanceRecordBase):
    id: int
    class Config:
        orm_mode = True
