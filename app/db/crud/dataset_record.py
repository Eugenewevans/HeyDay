from sqlalchemy.orm import Session

from app.db.models.dataset_record import DatasetRecord
from app.db.schemas.dataset_record import DatasetRecordCreate, DatasetRecordUpdate


def create_record(db: Session, data: DatasetRecordCreate) -> DatasetRecord:
    r = DatasetRecord(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def get_record(db: Session, record_id: int) -> DatasetRecord | None:
    return db.get(DatasetRecord, record_id)


def list_records(db: Session, dataset_id: int, limit: int = 100) -> list[DatasetRecord]:
    return (
        db.query(DatasetRecord)
        .filter(DatasetRecord.dataset_id == dataset_id)
        .order_by(DatasetRecord.id.desc())
        .limit(limit)
        .all()
    )


def update_record(db: Session, record: DatasetRecord, data: DatasetRecordUpdate) -> DatasetRecord:
    record.data = data.data
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record: DatasetRecord) -> None:
    db.delete(record)
    db.commit()

