from sqlalchemy.orm import Session

from app.db.models.dataset_field_map import DatasetFieldMap
from app.db.schemas.dataset_field_map import DatasetFieldMapCreate, DatasetFieldMapUpdate


def upsert_mapping(db: Session, data: DatasetFieldMapCreate) -> DatasetFieldMap:
    m = (
        db.query(DatasetFieldMap)
        .filter(DatasetFieldMap.dataset_id == data.dataset_id, DatasetFieldMap.role == data.role)
        .first()
    )
    if m:
        m.source_column = data.source_column
        db.add(m)
    else:
        m = DatasetFieldMap(**data.model_dump())
        db.add(m)
    db.commit()
    db.refresh(m)
    return m


def list_mappings(db: Session, dataset_id: int) -> list[DatasetFieldMap]:
    return db.query(DatasetFieldMap).filter(DatasetFieldMap.dataset_id == dataset_id).all()

