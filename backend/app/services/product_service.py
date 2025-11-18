# app/services/product_service.py
from fastapi import HTTPException
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def list_products(self):
        return await self.repo.get_all()

    async def get_product(self, product_id: int):
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(404, "Product not found")
        return product

    async def create_product(self, data):
        # contoh validasi
        if data.price < 0:
            raise HTTPException(400, "Price cannot be negative")

        return await self.repo.create(data)

    async def update_product(self, product_id: int, data):
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        return await self.repo.update(product, data)

    async def delete_product(self, product_id: int):
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        await self.repo.delete(product)
        return {"message": "Product deleted"}
