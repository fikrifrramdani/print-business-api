from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.print_size_conversion import PrintSizeConversion

router = APIRouter(prefix="/print-size-conversions", tags=["Print Size Conversion"])

@router.get("/")
def get_conversions(db: Session = Depends(get_db)):
    return db.query(PrintSizeConversion).all()

@router.post("/")
def create_conversion(data: dict, db: Session = Depends(get_db)):
    new_data = PrintSizeConversion(**data)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data
