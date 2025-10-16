from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.db.crud.dataset import list_dataset_customers
from app.db.models.automation import Automation
from app.db.models.consent import Consent
from app.db.models.message import Message
from app.db.models.template import Template
from app.services.ai import AIService
from app.services.messaging import SMSProvider, EmailProvider
from app.db.session import SessionLocal


def _parse_time(hhmm: str) -> tuple[int, int]:
    hh, mm = hhmm.split(":")
    return int(hh), int(mm)


def plan_upcoming_messages() -> int:
    """Create Message rows for active automations scheduled for today (planned)."""
    db: Session = SessionLocal()
    try:
        today = date.today()
        created = 0
        for a in db.query(Automation).filter(Automation.active == True).all():  # noqa: E712
            # For MVP: assume event date is customer's birthday; schedule on date + offset
            customers = list_dataset_customers(db, a.dataset_id)
            hh, mm = _parse_time(a.send_time)
            for c in customers:
                event_date = c.birthday  # extend later per event type
                if not event_date:
                    continue
                scheduled_date = event_date + timedelta(days=a.day_offset)
                if scheduled_date.month == today.month and scheduled_date.day == today.day:
                    scheduled_dt = datetime.combine(today, datetime.min.time()).replace(hour=hh, minute=mm)
                    # Consent check: require opt_in for channel if any record exists; default opt_in if none.
                    consent = (
                        db.query(Consent)
                        .filter(Consent.customer_id == c.id, Consent.channel == a.channel)
                        .order_by(Consent.updated_at.desc())
                        .first()
                    )
                    if consent and consent.status == "opt_out":
                        continue
                    msg = Message(
                        automation_id=a.id,
                        customer_id=c.id,
                        channel=a.channel,
                        status="planned",
                        scheduled_for=scheduled_dt,
                    )
                    db.add(msg)
                    created += 1
        db.commit()
        return created
    finally:
        db.close()


def dispatch_due_messages() -> int:
    """Generate content for due messages and simulate send; mark as sent/failed."""
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        due = db.query(Message).filter(Message.status == "planned", Message.scheduled_for <= now).all()
        sms = SMSProvider()
        email = EmailProvider()
        ai = AIService()
        for m in due:
            # Fill content from template + AI if empty
            if not m.body:
                tpl = db.get(Template, m.automation_id and db.get(Message, m.id).automation_id)
            # Fallback simple template lookup by automation->template
            from app.db.models.automation import Automation
            a = db.get(Automation, m.automation_id) if m.automation_id else None
            tpl = db.get(Template, a.template_id) if a else None
            prompt = (tpl.content if tpl else "Hello {{name}}")
            # For now, we don't hydrate variables from contact; just simple name placeholder
            from app.db.models.customer import Customer
            c = db.get(Customer, m.customer_id)
            variables = {"name": c.name if c else "there"}
            for k, v in variables.items():
                prompt = prompt.replace("{{"+k+"}}", v)
            body = ai.generate_message(prompt)
            m.body = body
            m.status = "queued"
            db.add(m)
            # Simulate send
            ok = True
            if m.channel == "sms" and c and c.phone:
                ok = sms.send_sms(c.phone, body)
            elif m.channel == "email" and c and c.email:
                ok = email.send_email(c.email, subject=tpl.name if tpl else "HeyDay", html=body)
            else:
                ok = False
            m.status = "sent" if ok else "failed"
            db.add(m)
        db.commit()
        return len(due)
    finally:
        db.close()

