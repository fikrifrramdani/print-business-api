from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.stock_movement import StockMovement
from app.models.product import Product
from app.schemas.stock_movement_schemas import StockMovementCreate, StockMovementResponse
from typing import List

router = APIRouter(prefix="/stock-movement", tags=["Stock Movement"])


@router.get("/", response_model=List[StockMovementResponse])
def get_all_movement(db: Session = Depends(get_db)):
    return db.query(StockMovement).order_by(StockMovement.id.desc()).all()


@router.post("/", response_model=StockMovementResponse)
def create_movement(data: StockMovementCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update stock
    if data.type == "in":
        product.stock += data.quantity
    elif data.type == "out":
        if product.stock < data.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")
        product.stock -= data.quantity
    else:
        raise HTTPException(400, "Invalid type (must be 'in' or 'out')")

    movement = StockMovement(
        product_id=data.product_id,
        type=data.type,
        quantity=data.quantity,
        note=data.note,
        reference_id=data.reference_id
    )

    db.add(movement)
    db.commit()
    db.refresh(movement)

    return movement


@router.get("/by-product/{product_id}", response_model=List[StockMovementResponse])
def get_by_product(product_id: int, db: Session = Depends(get_db)):
    return db.query(StockMovement).filter(StockMovement.product_id == product_id).all()
