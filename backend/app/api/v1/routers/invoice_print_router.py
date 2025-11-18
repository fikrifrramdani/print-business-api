from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice_print import InvoicePrint

router = APIRouter(prefix="/invoice-print", tags=["Invoice Print"])

@router.get("/")
def get_invoices(db: Session = Depends(get_db)):
    return db.query(InvoicePrint).all()

@router.post("/")
def create_invoice(data: dict, db: Session = Depends(get_db)):
    invoice = InvoicePrint(**data)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice
