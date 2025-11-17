# app/crud/customer.py
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

def get_customers(db: Session):
    return db.query(Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def create_customer(db: Session, data: CustomerCreate):
    new_customer = Customer(**data.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def update_customer(db: Session, customer_id: int, data: CustomerUpdate):
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True
