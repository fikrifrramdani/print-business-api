from sqlalchemy.orm import Session
from app.models.stock_movement import StockMovement
from app.models.product import Product
from app.schemas.stock_movement_schemas import StockMovementCreate

def create_stock_movement(db: Session, data: StockMovementCreate):
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise ValueError("Product not found")

    # Update stok
    if data.movement_type == "IN":
        product.stock += data.quantity
    elif data.movement_type == "OUT":
        if product.stock < data.quantity:
            raise ValueError("Not enough stock")
        product.stock -= data.quantity
    else:
        raise ValueError("Invalid movement type")

    movement = StockMovement(**data.dict())
    db.add(movement)
    db.commit()
    db.refresh(movement)

    return movement
