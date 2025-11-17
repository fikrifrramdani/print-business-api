from pydantic import BaseModel
from datetime import datetime

class StockMovementBase(BaseModel):
    product_id: int
    type: str  # in / out
    quantity: int
    note: str | None = None
    reference_id: int | None = None

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementResponse(StockMovementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
