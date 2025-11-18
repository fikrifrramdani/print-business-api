from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.print_material import PrintMaterial

router = APIRouter(prefix="/print-materials", tags=["Print Materials"])

@router.get("/")
def get_materials(db: Session = Depends(get_db)):
    return db.query(PrintMaterial).all()

@router.post("/")
def create_material(data: dict, db: Session = Depends(get_db)):
    new_data = PrintMaterial(**data)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data
