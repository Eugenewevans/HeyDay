from sqlalchemy.orm import Session

from app.db.models.customer import Customer
from app.db.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, data: CustomerCreate) -> Customer:
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


def list_customers(db: Session, skip: int = 0, limit: int = 100) -> list[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer: Customer, data: CustomerUpdate) -> Customer:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: Customer) -> None:
    db.delete(customer)
    db.commit()

