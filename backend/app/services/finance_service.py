from sqlalchemy.orm import Session
from datetime import date
from app.models.finance import FinanceRecord, FinanceCategory

def get_financial_summary(db: Session, period: str = None):
    """Hitung total income, expense, dan saldo bersih."""
    if not period:
        period = date.today().strftime("%b-%y")

    income = (
        db.query(FinanceRecord)
        .join(FinanceCategory)
        .filter(FinanceCategory.type == "income", FinanceRecord.period == period)
        .all()
    )
    expense = (
        db.query(FinanceRecord)
        .join(FinanceCategory)
        .filter(FinanceCategory.type == "expense", FinanceRecord.period == period)
        .all()
    )

    total_income = sum(r.amount for r in income)
    total_expense = sum(r.amount for r in expense)
    net = total_income - total_expense

    return {
        "period": period,
        "income_total": total_income,
        "expense_total": total_expense,
        "net_balance": net,
        "income_count": len(income),
        "expense_count": len(expense)
    }
