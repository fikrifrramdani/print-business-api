# app/modules/product/repository.py
from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, data):
        new = Product(
            name=data.name,
            category=data.category,
            description=data.description,
            price=data.price
        )
        self.db.add(new)
        self.db.commit()
        self.db.refresh(new)
        return new

    def update(self, product: Product, updates: dict):
        for k, v in updates.items():
            setattr(product, k, v)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.commit()
