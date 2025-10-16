from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud.automation import (
    create_automation,
    delete_automation,
    get_automation,
    list_automations,
    update_automation,
)
from app.db.schemas.automation import AutomationCreate, AutomationOut, AutomationUpdate
from app.db.session import get_db


router = APIRouter(prefix="/automations", tags=["automations"])


@router.post("/", response_model=AutomationOut)
def create(data: AutomationCreate, db: Session = Depends(get_db)):
    return create_automation(db, data)


@router.get("/", response_model=list[AutomationOut])
def list_(db: Session = Depends(get_db)):
    return list_automations(db)


@router.get("/{automation_id}", response_model=AutomationOut)
def get(automation_id: int, db: Session = Depends(get_db)):
    a = get_automation(db, automation_id)
    if not a:
        raise HTTPException(status_code=404, detail="Automation not found")
    return a


@router.put("/{automation_id}", response_model=AutomationOut)
def update(automation_id: int, data: AutomationUpdate, db: Session = Depends(get_db)):
    a = get_automation(db, automation_id)
    if not a:
        raise HTTPException(status_code=404, detail="Automation not found")
    return update_automation(db, a, data)


@router.delete("/{automation_id}")
def delete(automation_id: int, db: Session = Depends(get_db)):
    a = get_automation(db, automation_id)
    if not a:
        raise HTTPException(status_code=404, detail="Automation not found")
    delete_automation(db, a)
    return {"deleted": True}

