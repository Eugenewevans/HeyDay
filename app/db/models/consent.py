from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Consent(Base):
    __tablename__ = "consents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), index=True)
    channel: Mapped[str] = mapped_column(String(10))  # sms|email
    status: Mapped[str] = mapped_column(String(10), default="opt_in")  # opt_in|opt_out
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)  # where consent came from
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

