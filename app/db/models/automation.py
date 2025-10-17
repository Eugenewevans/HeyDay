from datetime import time

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Automation(Base):
    __tablename__ = "automations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    event_type_id: Mapped[int] = mapped_column(ForeignKey("event_types.id", ondelete="RESTRICT"), index=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id", ondelete="RESTRICT"), index=True)

    # Trigger configuration
    trigger_column_name: Mapped[str] = mapped_column(String(100), nullable=False)  # which date column drives this
    day_offset: Mapped[int] = mapped_column(Integer, default=0)
    send_time: Mapped[str] = mapped_column(String(5), default="09:00")  # HH:MM 24h
    channel: Mapped[str] = mapped_column(String(10), default="sms")  # sms|email
    mode: Mapped[str] = mapped_column(String(10), default="preview")  # preview|auto
    active: Mapped[bool] = mapped_column(Boolean, default=False)

