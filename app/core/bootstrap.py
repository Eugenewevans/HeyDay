from sqlalchemy.orm import Session

from app.db.models.event_type import EventType
from app.db.session import SessionLocal


def seed_event_types() -> None:
    db: Session = SessionLocal()
    try:
        if not db.query(EventType).filter(EventType.key == "birthday").first():
            db.add(EventType(key="birthday", name="Birthday"))
            db.commit()
    finally:
        db.close()

