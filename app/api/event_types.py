from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud.event_type import (
    create_event_type,
    delete_event_type,
    get_event_type,
    list_event_types,
    update_event_type,
)
from app.db.schemas.event_type import EventTypeCreate, EventTypeOut, EventTypeUpdate
from app.db.session import get_db


router = APIRouter(prefix="/event-types", tags=["event_types"])


@router.post("/", response_model=EventTypeOut)
def create(data: EventTypeCreate, db: Session = Depends(get_db)):
    return create_event_type(db, data)


@router.get("/", response_model=list[EventTypeOut])
def list_(db: Session = Depends(get_db)):
    return list_event_types(db)


@router.get("/{event_type_id}", response_model=EventTypeOut)
def get(event_type_id: int, db: Session = Depends(get_db)):
    et = get_event_type(db, event_type_id)
    if not et:
        raise HTTPException(status_code=404, detail="EventType not found")
    return et


@router.put("/{event_type_id}", response_model=EventTypeOut)
def update(event_type_id: int, data: EventTypeUpdate, db: Session = Depends(get_db)):
    et = get_event_type(db, event_type_id)
    if not et:
        raise HTTPException(status_code=404, detail="EventType not found")
    return update_event_type(db, et, data)


@router.delete("/{event_type_id}")
def delete(event_type_id: int, db: Session = Depends(get_db)):
    et = get_event_type(db, event_type_id)
    if not et:
        raise HTTPException(status_code=404, detail="EventType not found")
    delete_event_type(db, et)
    return {"deleted": True}

