# app/modules/product/service.py
from fastapi import HTTPException
from app.modules.product.repository import ProductRepository

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def list_products(self):
        return self.repo.list_all()

    def get_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def create_product(self, data):
        if data.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")
        return self.repo.create(data)

    def update_product(self, product_id: int, data):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        updates = data.dict(exclude_unset=True)
        return self.repo.update(product, updates)

    def delete_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        self.repo.delete(product)
        return {"message": "Product deleted"}
