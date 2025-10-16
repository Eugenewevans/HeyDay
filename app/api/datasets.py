from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud.dataset import (
    add_customer_to_dataset,
    create_dataset,
    delete_dataset,
    get_dataset,
    list_dataset_customers,
    list_datasets,
    remove_customer_from_dataset,
    update_dataset,
)
from app.db.schemas.dataset import DatasetCreate, DatasetOut, DatasetUpdate
from app.db.schemas.customer import CustomerOut
from app.db.session import get_db


router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", response_model=DatasetOut)
def create(data: DatasetCreate, db: Session = Depends(get_db)):
    return create_dataset(db, data)


@router.get("/", response_model=list[DatasetOut])
def list_(db: Session = Depends(get_db)):
    return list_datasets(db)


@router.get("/{dataset_id}", response_model=DatasetOut)
def get(dataset_id: int, db: Session = Depends(get_db)):
    ds = get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds


@router.put("/{dataset_id}", response_model=DatasetOut)
def update(dataset_id: int, data: DatasetUpdate, db: Session = Depends(get_db)):
    ds = get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return update_dataset(db, ds, data)


@router.delete("/{dataset_id}")
def delete(dataset_id: int, db: Session = Depends(get_db)):
    ds = get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    delete_dataset(db, ds)
    return {"deleted": True}


@router.post("/{dataset_id}/customers/{customer_id}")
def add_customer(dataset_id: int, customer_id: int, db: Session = Depends(get_db)):
    add_customer_to_dataset(db, dataset_id, customer_id)
    return {"added": True}


@router.delete("/{dataset_id}/customers/{customer_id}")
def remove_customer(dataset_id: int, customer_id: int, db: Session = Depends(get_db)):
    remove_customer_from_dataset(db, dataset_id, customer_id)
    return {"removed": True}


@router.get("/{dataset_id}/customers", response_model=list[CustomerOut])
def list_customers(dataset_id: int, db: Session = Depends(get_db)):
    return list_dataset_customers(db, dataset_id)

