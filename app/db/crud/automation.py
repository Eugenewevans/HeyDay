from sqlalchemy.orm import Session

from app.db.models.automation import Automation
from app.db.schemas.automation import AutomationCreate, AutomationUpdate


def create_automation(db: Session, data: AutomationCreate) -> Automation:
    a = Automation(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def get_automation(db: Session, automation_id: int) -> Automation | None:
    return db.get(Automation, automation_id)


def list_automations(db: Session) -> list[Automation]:
    return db.query(Automation).order_by(Automation.id.desc()).all()


def update_automation(db: Session, automation: Automation, data: AutomationUpdate) -> Automation:
    for f, v in data.model_dump(exclude_unset=True).items():
        setattr(automation, f, v)
    db.add(automation)
    db.commit()
    db.refresh(automation)
    return automation


def delete_automation(db: Session, automation: Automation) -> None:
    db.delete(automation)
    db.commit()

