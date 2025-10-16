from sqlalchemy.orm import Session

from app.db.models.message import Message
from app.db.schemas.message import MessageCreate, MessageUpdate


def create_message(db: Session, data: MessageCreate) -> Message:
    m = Message(**data.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def get_message(db: Session, message_id: int) -> Message | None:
    return db.get(Message, message_id)


def list_messages(db: Session, status: str | None = None) -> list[Message]:
    q = db.query(Message).order_by(Message.id.desc())
    if status:
        q = q.filter(Message.status == status)
    return q.all()


def update_message(db: Session, msg: Message, data: MessageUpdate) -> Message:
    for f, v in data.model_dump(exclude_unset=True).items():
        setattr(msg, f, v)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def delete_message(db: Session, msg: Message) -> None:
    db.delete(msg)
    db.commit()

