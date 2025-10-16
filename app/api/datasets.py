from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
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
from app.db.schemas.customer import CustomerCreate
import csv
import io
from datetime import datetime


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


def _get(row: dict, keys: list[str]) -> str | None:
    for k in keys:
        if k in row and row[k]:
            return row[k]
    return None


def _normalize_headers(headers: list[str]) -> list[str]:
    return [h.strip().lower() for h in headers]


def _parse_date(value: str | None) -> datetime.date | None:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


@router.post("/{dataset_id}/import/csv")
async def import_csv(dataset_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    ds = get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    content = await file.read()
    text = content.decode("utf-8-sig", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    reader.fieldnames = _normalize_headers(reader.fieldnames or [])
    name_keys = ["name", "full name", "customer name"]
    email_keys = ["email", "e-mail"]
    phone_keys = ["phone", "phone number", "mobile"]
    bday_keys = ["birthday", "dob", "date of birth", "birthdate"]

    created = 0
    for row in reader:
        row_l = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        data = CustomerCreate(
            name=_get(row_l, name_keys) or "",
            email=_get(row_l, email_keys),
            phone=_get(row_l, phone_keys),
            birthday=_parse_date(_get(row_l, bday_keys)),
        )
        if not data.name:
            continue
        # create and link
        from app.db.crud.customer import create_customer  # local import to avoid cycles

        c = create_customer(db, data)
        add_customer_to_dataset(db, dataset_id, c.id)
        created += 1

    return {"imported": created}


@router.post("/{dataset_id}/import/json")
def import_json(dataset_id: int, items: list[CustomerCreate], db: Session = Depends(get_db)):
    ds = get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    from app.db.crud.customer import create_customer

    created = 0
    for data in items:
        c = create_customer(db, data)
        add_customer_to_dataset(db, dataset_id, c.id)
        created += 1
    return {"imported": created}

