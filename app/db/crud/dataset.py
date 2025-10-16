from sqlalchemy.orm import Session

from app.db.models.associations import dataset_customers
from app.db.models.dataset import Dataset
from app.db.models.customer import Customer
from app.db.schemas.dataset import DatasetCreate, DatasetUpdate


def create_dataset(db: Session, data: DatasetCreate) -> Dataset:
    ds = Dataset(**data.model_dump())
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds


def get_dataset(db: Session, dataset_id: int) -> Dataset | None:
    return db.get(Dataset, dataset_id)


def list_datasets(db: Session) -> list[Dataset]:
    return db.query(Dataset).order_by(Dataset.id.desc()).all()


def update_dataset(db: Session, ds: Dataset, data: DatasetUpdate) -> Dataset:
    for f, v in data.model_dump(exclude_unset=True).items():
        setattr(ds, f, v)
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds


def delete_dataset(db: Session, ds: Dataset) -> None:
    db.delete(ds)
    db.commit()


def add_customer_to_dataset(db: Session, dataset_id: int, customer_id: int) -> None:
    db.execute(dataset_customers.insert().values(dataset_id=dataset_id, customer_id=customer_id))
    db.commit()


def remove_customer_from_dataset(db: Session, dataset_id: int, customer_id: int) -> None:
    db.execute(
        dataset_customers.delete().where(
            (dataset_customers.c.dataset_id == dataset_id) & (dataset_customers.c.customer_id == customer_id)
        )
    )
    db.commit()


def list_dataset_customers(db: Session, dataset_id: int) -> list[Customer]:
    return (
        db.query(Customer)
        .join(dataset_customers, dataset_customers.c.customer_id == Customer.id)
        .filter(dataset_customers.c.dataset_id == dataset_id)
        .all()
    )

