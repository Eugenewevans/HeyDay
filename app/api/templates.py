from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud.template import (
    create_template,
    delete_template,
    get_template,
    list_templates,
    update_template,
)
from app.db.schemas.template import TemplateCreate, TemplateOut, TemplateUpdate
from app.db.session import get_db


router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("/", response_model=TemplateOut)
def create(data: TemplateCreate, db: Session = Depends(get_db)):
    return create_template(db, data)


@router.get("/", response_model=list[TemplateOut])
def list_(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_templates(db, skip=skip, limit=limit)


@router.get("/{template_id}", response_model=TemplateOut)
def get(template_id: int, db: Session = Depends(get_db)):
    template = get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put("/{template_id}", response_model=TemplateOut)
def update(template_id: int, data: TemplateUpdate, db: Session = Depends(get_db)):
    template = get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return update_template(db, template, data)


@router.delete("/{template_id}")
def delete(template_id: int, db: Session = Depends(get_db)):
    template = get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    delete_template(db, template)
    return {"deleted": True}

