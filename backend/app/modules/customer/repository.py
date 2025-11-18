# app/modules/customer/repository.py
from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        return self.db.query(Customer).all()

    def get_by_id(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def create(self, data):
        new = Customer(
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address
        )
        self.db.add(new)
        self.db.commit()
        self.db.refresh(new)
        return new

    def update(self, customer: Customer, updates: dict):
        for k, v in updates.items():
            setattr(customer, k, v)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer: Customer):
        self.db.delete(customer)
        self.db.commit()
