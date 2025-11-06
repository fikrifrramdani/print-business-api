# app/seeders/product_seeder.py
from app.models.product import ProductCategory, Product

def seed_products(db):
    if not db.query(ProductCategory).first():
        cat = ProductCategory(name="Default")
        db.add(cat)
        db.commit()
        db.refresh(cat)

        sample = Product(
            code="P001",
            name="Print Warna A4",
            type="jasa",
            cost_price=1000,
            sell_price=2000,
            profit=1000,
            profit_percent=100,
            category_id=cat.id,
            stock=0
        )
        db.add(sample)
        db.commit()
