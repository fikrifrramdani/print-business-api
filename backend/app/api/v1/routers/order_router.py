from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from app.db.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.finance import FinanceRecord, FinanceCategory

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.post("/")
def add_order(
    order_number: str,
    customer_name: str,
    store_id: int,
    items: list[dict],
    db: Session = Depends(get_db)
):
    # Cegah duplikat order
    existing = db.query(Order).filter(Order.order_number == order_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nomor order sudah digunakan")

    order = Order(
        platform="Manual",
        order_number=order_number,
        order_date=date.today(),
        customer_name=customer_name,
        status="Design",
        store_id=store_id
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    total_order = 0
    for i in items:
        product = db.query(Product).filter(Product.id == i["product_id"]).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produk ID {i['product_id']} tidak ditemukan")
        if product.stock < i["quantity"]:
            raise HTTPException(status_code=400, detail=f"Stok '{product.name}' tidak cukup")

        total = product.sell_price * i["quantity"]
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=i["quantity"],
            price=product.sell_price,
            total=total
        )
        db.add(item)

        product.stock -= i["quantity"]  # 🔻 kurangi stok
        total_order += total

    db.commit()

    # Catat keuangan otomatis
    category = (
        db.query(FinanceCategory)
        .filter(FinanceCategory.name == "Penjualan", FinanceCategory.type == "income")
        .first()
    )
    if not category:
        category = FinanceCategory(name="Penjualan", type="income")
        db.add(category)
        db.commit()
        db.refresh(category)

    record = FinanceRecord(
        category_id=category.id,
        amount=total_order,
        note=f"Order #{order.order_number} - {customer_name}",
        source="Sales Order",
        date=date.today(),
        period=date.today().strftime("%b-%y")
    )
    db.add(record)
    db.commit()

    return {
        "message": "Order berhasil dibuat dan stok diperbarui",
        "order_id": order.id,
        "total": total_order
    }

@router.get("/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return {"order": order, "items": items}

# --- ❌ Hapus order dengan rollback aman ---
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        # 🔹 1️⃣ Cek order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order tidak ditemukan")

        # 🔹 2️⃣ Ambil semua item order
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        # 🔹 3️⃣ Kembalikan stok produk
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity  # 🔁 kembalikan stok
            db.delete(item)

        # 🔹 4️⃣ Hapus catatan keuangan terkait order ini
        record = (
            db.query(FinanceRecord)
            .filter(FinanceRecord.note.like(f"%#{order.order_number}%"))
            .first()
        )
        if record:
            db.delete(record)

        # 🔹 5️⃣ Hapus order
        db.delete(order)
        db.commit()

        return {
            "message": f"Order #{order.order_number} berhasil dihapus",
            "stok_dikembalikan": True,
            "keuangan_dihapus": bool(record)
        }

    except SQLAlchemyError as e:
        db.rollback()  # 🚨 Batalkan semua perubahan jika error
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menghapus order. Perubahan dibatalkan. Error: {str(e)}"
        )
