from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class DatasetSchema(Base):
    __tablename__ = "dataset_schemas"
    __table_args__ = (UniqueConstraint("dataset_id", "column_name", name="uq_dataset_column"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    column_name: Mapped[str] = mapped_column(String(100), nullable=False)
    semantic_role: Mapped[str | None] = mapped_column(String(50), nullable=True)  # name|email|phone|date|text|number
    is_trigger_candidate: Mapped[bool] = mapped_column(Boolean, default=False)

