# app/seeders/finance_seeder.py
from app.models.finance import FinanceCategory
from sqlalchemy.orm import Session

def seed_finance_data(db: Session):
    categories = [
        {"name": "Penjualan", "type": "income"},
        {"name": "Modal", "type": "income"},
        {"name": "Operasional", "type": "expense"},
        {"name": "Gaji Karyawan", "type": "expense"},
    ]

    for cat in categories:
        exists = (
            db.query(FinanceCategory)
            .filter(FinanceCategory.name == cat["name"])
            .first()
        )
        if not exists:
            db.add(FinanceCategory(**cat))
    db.commit()
