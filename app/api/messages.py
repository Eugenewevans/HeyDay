from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud.message import (
    create_message,
    delete_message,
    get_message,
    list_messages,
    update_message,
)
from app.db.schemas.message import MessageCreate, MessageOut, MessageUpdate
from app.db.session import get_db
from app.services.ai import AIService
from app.db.models.message import Message as MessageModel


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageOut)
def create(data: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db, data)


@router.get("/", response_model=list[MessageOut])
def list_(status: str | None = None, db: Session = Depends(get_db)):
    return list_messages(db, status=status)


@router.get("/{message_id}", response_model=MessageOut)
def get(message_id: int, db: Session = Depends(get_db)):
    m = get_message(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    return m


@router.put("/{message_id}", response_model=MessageOut)
def update(message_id: int, data: MessageUpdate, db: Session = Depends(get_db)):
    m = get_message(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    return update_message(db, m, data)


@router.delete("/{message_id}")
def delete(message_id: int, db: Session = Depends(get_db)):
    m = get_message(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    delete_message(db, m)
    return {"deleted": True}


@router.post("/preview")
def preview_prompt(template: str, variables: dict[str, str] | None = None):
    prompt = template
    if variables:
        for k, v in variables.items():
            prompt = prompt.replace("{{" + k + "}}", v)
    text = AIService().generate_message(prompt)
    return {"preview": text}


@router.post("/{message_id}/approve", response_model=MessageOut)
def approve(message_id: int, db: Session = Depends(get_db)):
    m = get_message(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    m.status = "queued"
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.post("/{message_id}/cancel", response_model=MessageOut)
def cancel(message_id: int, db: Session = Depends(get_db)):
    m = get_message(db, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message not found")
    m.status = "failed"
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

