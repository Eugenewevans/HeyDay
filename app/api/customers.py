from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud.customer import (
    create_customer,
    delete_customer,
    get_customer,
    list_customers,
    update_customer,
)
from app.db.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from app.db.session import get_db


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerOut)
def create(data: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, data)


@router.get("/", response_model=list[CustomerOut])
def list_(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_customers(db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerOut)
def get(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=CustomerOut)
def update(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return update_customer(db, customer, data)


@router.delete("/{customer_id}")
def delete(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(db, customer)
    return {"deleted": True}

