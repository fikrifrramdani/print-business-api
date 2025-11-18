from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.print_job import PrintJob

router = APIRouter(prefix="/print-jobs", tags=["Print Jobs"])

@router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(PrintJob).all()

@router.post("/")
def create_job(data: dict, db: Session = Depends(get_db)):
    new_job = PrintJob(**data)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job
