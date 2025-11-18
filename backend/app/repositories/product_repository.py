# app/repositories/product_repositories.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.product import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, product_id: int):
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()

    async def create(self, data):
        product = Product(
            name=data.name,
            category=data.category,
            description=data.description,
            price=data.price,
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product: Product, data):
        if data.name is not None:
            product.name = data.name
        if data.category is not None:
            product.category = data.category
        if data.description is not None:
            product.description = data.description
        if data.price is not None:
            product.price = data.price

        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product):
        await self.db.delete(product)
        await self.db.commit()
        return True
