from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.finance import FinanceCategory, FinanceRecord
from fastapi import HTTPException
from datetime import datetime
from app.services.finance_service import get_financial_summary

router = APIRouter(prefix="/finance", tags=["Finance"])

# --- CATEGORY CRUD ---
@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(FinanceCategory).all()

@router.post("/categories")
def add_category(name: str, type: str, db: Session = Depends(get_db)):
    cat = FinanceCategory(name=name, type=type)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

# --- RECORD CRUD ---
@router.get("/records")
def get_records(db: Session = Depends(get_db)):
    return db.query(FinanceRecord).order_by(FinanceRecord.date.desc()).all()

@router.post("/records")
def add_record(
    category_id: int,
    amount: float,
    note: str,
    source: str,
    db: Session = Depends(get_db)
):
    record = FinanceRecord(
        category_id=category_id,
        amount=amount,
        note=note,
        source=source,
        date=date.today(),
        period=date.today().strftime("%b-%y")
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# --- RINGKASAN KEUANGAN ---
@router.get("/summary")
def finance_summary(db: Session = Depends(get_db)):
    summary = get_financial_summary(db)
    return summary

# 💸 3️⃣ Tambah pengeluaran manual
@router.post("/add-expense")
def add_expense(
    category_name: str,
    amount: float,
    note: str,
    db: Session = Depends(get_db)
):
    # cari kategori 'expense' dengan nama tertentu
    category = (
        db.query(FinanceCategory)
        .filter(FinanceCategory.name == category_name, FinanceCategory.type == "expense")
        .first()
    )

    # kalau belum ada, otomatis buat baru
    if not category:
        category = FinanceCategory(name=category_name, type="expense")
        db.add(category)
        db.commit()
        db.refresh(category)

    # buat record pengeluaran
    record = FinanceRecord(
        category_id=category.id,
        amount=amount,
        note=note,
        source="Manual Input",
        date=date.today(),
        period=date.today().strftime("%b-%y")
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "Pengeluaran berhasil ditambahkan",
        "id": record.id,
        "category": category_name,
        "amount": amount
    }

@router.get("/summary/{period}")
def finance_summary_by_period(period: str, db: Session = Depends(get_db)):
    return get_financial_summary(db, period)
