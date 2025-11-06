# # app/routers/product_router.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.product import Product, ProductCategory
# from app.schemas.product_schemas import ProductCreate

# router = APIRouter(prefix="/products", tags=["Products"])

# # --- CATEGORY CRUD ---
# @router.get("/categories")
# def get_categories(db: Session = Depends(get_db)):
#     return db.query(ProductCategory).all()

# @router.post("/categories")
# def add_category(name: str, db: Session = Depends(get_db)):
#     cat = ProductCategory(name=name)
#     db.add(cat)
#     db.commit()
#     db.refresh(cat)
#     return cat

# # --- PRODUCT CRUD ---
# @router.get("/")
# def get_products(db: Session = Depends(get_db)):
#     return db.query(Product).all()

# # ----------------------------
# # GET: Produk berdasarkan ID
# # ----------------------------
# @router.get("/{product_id}")
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
#     return product

# # ----------------------------
# # POST: Tambah produk baru
# # ----------------------------
# @router.post("/")
# def add_product(data: ProductCreate, db: Session = Depends(get_db)):
#     existing = db.query(Product).filter(Product.code == data.code).first()
#     if existing:
#         raise HTTPException(status_code=400, detail=f"Kode produk '{data.code}' sudah digunakan")

#     profit = data.sell_price - data.cost_price
#     profit_percent = (profit / data.cost_price * 100) if data.cost_price else 0

#     product = Product(
#         code=data.code,
#         name=data.name,
#         type=data.type,
#         cost_price=data.cost_price,
#         sell_price=data.sell_price,
#         profit=profit,
#         profit_percent=profit_percent,
#         category_id=data.category_id,
#         stock=data.stock or 0
#     )

#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     return product

# # ----------------------------
# # PUT: Update data produk
# # ----------------------------
# @router.put("/{product_id}")
# def update_product(product_id: int, name: str, cost_price: float, sell_price: float, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

#     product.name = name
#     product.cost_price = cost_price
#     product.sell_price = sell_price
#     product.profit = sell_price - cost_price
#     product.profit_percent = (product.profit / cost_price * 100) if cost_price else 0
#     db.commit()
#     db.refresh(product)
#     return product

# # ----------------------------
# # DELETE: Hapus produk
# # ----------------------------
# @router.delete("/{product_id}")
# def delete_product(product_id: int, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
#     db.delete(product)
#     db.commit()
#     return {"message": "Produk dihapus"}

# @router.put("/{product_id}/stock")
# def update_stock(product_id: int, stock: int, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

#     product.stock = stock
#     db.commit()
#     db.refresh(product)
#     return {"message": "Stok diperbarui", "product": product}

# @router.get("/by-category/{category_id}")
# def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
#     products = db.query(Product).filter(Product.category_id == category_id).all()
#     return products

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product, ProductCategory
from app.schemas.product_schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    CategoryCreate, CategoryResponse
)
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

# ==========================
# CATEGORY CRUD
# ==========================
@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(ProductCategory).all()

@router.post("/categories", response_model=CategoryResponse)
def add_category(data: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(ProductCategory).filter(ProductCategory.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Kategori '{data.name}' sudah ada")
    cat = ProductCategory(name=data.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


# ==========================
# PRODUCT CRUD
# ==========================
@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product

@router.post("/", response_model=ProductResponse)
def add_product(data: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Kode produk '{data.code}' sudah digunakan")

    profit = data.sell_price - data.cost_price
    profit_percent = (profit / data.cost_price * 100) if data.cost_price else 0

    product = Product(
        code=data.code,
        name=data.name,
        type=data.type,
        cost_price=data.cost_price,
        sell_price=data.sell_price,
        profit=profit,
        profit_percent=profit_percent,
        category_id=data.category_id,
        stock=data.stock or 0,
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    # hitung ulang profit
    if data.cost_price or data.sell_price:
        cost = data.cost_price or product.cost_price
        sell = data.sell_price or product.sell_price
        product.profit = sell - cost
        product.profit_percent = (product.profit / cost * 100) if cost else 0

    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    db.delete(product)
    db.commit()
    return None

@router.put("/{product_id}/stock")
def update_stock(product_id: int, stock: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    product.stock = stock
    db.commit()
    db.refresh(product)
    return {"message": "Stok diperbarui", "product": product}

@router.get("/by-category/{category_id}", response_model=List[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_id == category_id).all()
    return products
