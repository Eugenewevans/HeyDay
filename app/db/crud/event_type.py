from sqlalchemy.orm import Session

from app.db.models.event_type import EventType
from app.db.schemas.event_type import EventTypeCreate, EventTypeUpdate


def create_event_type(db: Session, data: EventTypeCreate) -> EventType:
    et = EventType(**data.model_dump())
    db.add(et)
    db.commit()
    db.refresh(et)
    return et


def get_event_type(db: Session, event_type_id: int) -> EventType | None:
    return db.get(EventType, event_type_id)


def list_event_types(db: Session) -> list[EventType]:
    return db.query(EventType).order_by(EventType.id.asc()).all()


def update_event_type(db: Session, et: EventType, data: EventTypeUpdate) -> EventType:
    for f, v in data.model_dump(exclude_unset=True).items():
        setattr(et, f, v)
    db.add(et)
    db.commit()
    db.refresh(et)
    return et


def delete_event_type(db: Session, et: EventType) -> None:
    db.delete(et)
    db.commit()

