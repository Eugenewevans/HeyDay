from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class DatasetFieldMap(Base):
    __tablename__ = "dataset_field_maps"
    __table_args__ = (
        UniqueConstraint("dataset_id", "role", name="uq_dataset_role"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(50))  # name|email|phone|trigger_date
    source_column: Mapped[str] = mapped_column(String(100))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

