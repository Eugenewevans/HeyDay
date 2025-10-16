from sqlalchemy.orm import Session

from app.db.models.template import Template
from app.db.schemas.template import TemplateCreate, TemplateUpdate


def create_template(db: Session, data: TemplateCreate) -> Template:
    template = Template(**data.model_dump())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


def get_template(db: Session, template_id: int) -> Template | None:
    return db.get(Template, template_id)


def list_templates(db: Session, skip: int = 0, limit: int = 100) -> list[Template]:
    return db.query(Template).offset(skip).limit(limit).all()


def update_template(db: Session, template: Template, data: TemplateUpdate) -> Template:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(template, field, value)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


def delete_template(db: Session, template: Template) -> None:
    db.delete(template)
    db.commit()

