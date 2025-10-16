from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class EventType(Base):
    __tablename__ = "event_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # e.g., birthday, renewal
    name: Mapped[str] = mapped_column(String(100), nullable=False)

