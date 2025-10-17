from sqlalchemy.orm import Session

from app.db.models.dataset_schema import DatasetSchema
from app.db.schemas.dataset_schema import DatasetSchemaCreate, DatasetSchemaUpdate


def upsert_schema_column(db: Session, data: DatasetSchemaCreate) -> DatasetSchema:
    col = (
        db.query(DatasetSchema)
        .filter(DatasetSchema.dataset_id == data.dataset_id, DatasetSchema.column_name == data.column_name)
        .first()
    )
    if col:
        if data.semantic_role is not None:
            col.semantic_role = data.semantic_role
        col.is_trigger_candidate = data.is_trigger_candidate
        db.add(col)
    else:
        col = DatasetSchema(**data.model_dump())
        db.add(col)
    db.commit()
    db.refresh(col)
    return col


def list_schema_columns(db: Session, dataset_id: int) -> list[DatasetSchema]:
    return db.query(DatasetSchema).filter(DatasetSchema.dataset_id == dataset_id).all()


def delete_schema_column(db: Session, col: DatasetSchema) -> None:
    db.delete(col)
    db.commit()

