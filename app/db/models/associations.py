from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.models.base import Base


dataset_customers = Table(
    "dataset_customers",
    Base.metadata,
    Column("dataset_id", Integer, ForeignKey("datasets.id", ondelete="CASCADE"), primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id", ondelete="CASCADE"), primary_key=True),
)

