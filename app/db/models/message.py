from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    automation_id: Mapped[int | None] = mapped_column(ForeignKey("automations.id", ondelete="SET NULL"), index=True)
    record_id: Mapped[int] = mapped_column(ForeignKey("dataset_records.id", ondelete="CASCADE"), index=True)
    channel: Mapped[str] = mapped_column(String(10))  # sms|email
    status: Mapped[str] = mapped_column(String(15), default="pending")  # pending|generated|approved|sent|failed
    subject: Mapped[str | None] = mapped_column(String(200), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_for: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

