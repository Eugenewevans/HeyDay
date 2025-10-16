from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models.consent import Consent as ConsentModel
from app.db.schemas.consent import ConsentCreate, ConsentOut, ConsentUpdate
from app.db.session import get_db


router = APIRouter(prefix="/consents", tags=["consents"])


@router.post("/", response_model=ConsentOut)
def create(data: ConsentCreate, db: Session = Depends(get_db)):
    c = ConsentModel(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.get("/", response_model=list[ConsentOut])
def list_(db: Session = Depends(get_db)):
    return db.query(ConsentModel).all()


@router.put("/{consent_id}", response_model=ConsentOut)
def update(consent_id: int, data: ConsentUpdate, db: Session = Depends(get_db)):
    c = db.get(ConsentModel, consent_id)
    if not c:
        raise HTTPException(status_code=404, detail="Consent not found")
    for f, v in data.model_dump(exclude_unset=True).items():
        setattr(c, f, v)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

