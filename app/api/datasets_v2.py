"""New flexible dataset imports and schema management for Phase 1+"""
import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.crud.dataset import get_dataset
from app.db.crud.dataset_record import create_record
from app.db.crud.dataset_schema import upsert_schema_column, list_schema_columns
from app.db.schemas.dataset_record import DatasetRecordCreate
from app.db.schemas.dataset_schema import DatasetSchemaCreate, DatasetSchemaOut, DatasetSchemaUpdate
from app.db.session import get_db


router = APIRouter(prefix="/datasets-v2", tags=["datasets-v2"])


def _infer_semantic_role(col_name: str) -> tuple[str | None, bool]:
    """Return (semantic_role, is_trigger_candidate)"""
    col_lower = col_name.lower()
    if col_lower in ("name", "full name", "customer name"):
        return ("name", False)
    if col_lower in ("email", "e-mail"):
        return ("email", False)
    if col_lower in ("phone", "phone number", "mobile"):
        return ("phone", False)
    # Date-like columns are trigger candidates
    if any(kw in col_lower for kw in ("date", "birthday", "dob", "renewal", "anniversary")):
        return ("date", True)
    return (None, False)


@router.post("/{dataset_id}/import-flexible")
async def import_flexible_csv(dataset_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload CSV with flexible schema:
    - Detects all columns
    - Stores each row as JSON in dataset_records
    - Auto-infers semantic roles and trigger candidates
    - Returns detected schema for user confirmation
    """
    ds = get_dataset(db, dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")

    content = await file.read()
    text = content.decode("utf-8-sig", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    columns = reader.fieldnames or []

    # Detect schema
    detected_schema = []
    for col in columns:
        role, is_trigger = _infer_semantic_role(col)
        detected_schema.append({"column_name": col, "semantic_role": role, "is_trigger_candidate": is_trigger})
        # Save to DB
        upsert_schema_column(
            db, DatasetSchemaCreate(dataset_id=dataset_id, column_name=col, semantic_role=role, is_trigger_candidate=is_trigger)
        )

    # Import records
    created = 0
    for row in reader:
        data_dict = {k: (v.strip() if isinstance(v, str) and v else v) for k, v in row.items() if v}
        create_record(db, DatasetRecordCreate(dataset_id=dataset_id, data=data_dict))
        created += 1

    return {"imported": created, "detected_schema": detected_schema}


@router.get("/{dataset_id}/schema", response_model=list[DatasetSchemaOut])
def get_schema(dataset_id: int, db: Session = Depends(get_db)):
    return list_schema_columns(db, dataset_id)


@router.post("/{dataset_id}/schema")
def update_schema(dataset_id: int, columns: list[DatasetSchemaCreate], db: Session = Depends(get_db)):
    """User confirms/edits detected schema"""
    for col_data in columns:
        upsert_schema_column(db, col_data)
    return {"updated": len(columns)}

