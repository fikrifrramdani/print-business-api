# app/modules/customer/service.py
from fastapi import HTTPException
from app.modules.customer.repository import CustomerRepository

class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self.repo = repo

    def list_customers(self):
        return self.repo.list_all()

    def get_customer(self, customer_id: int):
        customer = self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    def create_customer(self, data):
        return self.repo.create(data)

    def update_customer(self, customer_id: int, data):
        customer = self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        updates = data.dict(exclude_unset=True)
        return self.repo.update(customer, updates)

    def delete_customer(self, customer_id: int):
        customer = self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        self.repo.delete(customer)
        return {"message": "Customer deleted"}
