from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice_retail import InvoiceRetail, InvoiceRetailItem

router = APIRouter(prefix="/invoice-retail", tags=["Invoice Retail"])

@router.get("/")
def get_retail_invoices(db: Session = Depends(get_db)):
    return db.query(InvoiceRetail).all()

@router.post("/")
def create_retail_invoice(data: dict, db: Session = Depends(get_db)):
    items = data.pop("items", [])

    invoice = InvoiceRetail(**data)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    # Tambah item invoice
    for item in items:
        invoice_item = InvoiceRetailItem(invoice_id=invoice.id, **item)
        db.add(invoice_item)

    db.commit()

    return {
        "invoice": invoice,
        "items": items
    }
