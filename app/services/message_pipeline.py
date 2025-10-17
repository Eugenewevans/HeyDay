"""Phase 4: Message generation pipeline (pending→generated→approved→sent)"""
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.db.crud.dataset_record import list_records
from app.db.crud.dataset_schema import list_schema_columns
from app.db.models.automation import Automation
from app.db.models.message import Message
from app.db.models.template import Template
from app.db.session import SessionLocal
from app.services.ai import AIService
from app.services.messaging import SMSProvider, EmailProvider


def _parse_time(hhmm: str) -> tuple[int, int]:
    hh, mm = hhmm.split(":")
    return int(hh), int(mm)


def plan_messages() -> int:
    """Create pending messages for active automations scheduled today"""
    db: Session = SessionLocal()
    try:
        today = date.today()
        created = 0
        for a in db.query(Automation).filter(Automation.active == True).all():  # noqa: E712
            schema = {c.column_name: c for c in list_schema_columns(db, a.dataset_id)}
            trigger_col = a.trigger_column_name
            if trigger_col not in schema:
                continue
            records = list_records(db, a.dataset_id, limit=1000)
            hh, mm = _parse_time(a.send_time)
            for rec in records:
                trigger_val = rec.data.get(trigger_col)
                if not trigger_val:
                    continue
                try:
                    event_date = datetime.strptime(str(trigger_val), "%Y-%m-%d").date()
                except Exception:
                    continue
                scheduled_date = event_date + timedelta(days=a.day_offset)
                if scheduled_date != today:
                    continue
                scheduled_dt = datetime.combine(today, datetime.min.time()).replace(hour=hh, minute=mm)
                # Check if message already exists
                existing = (
                    db.query(Message)
                    .filter(Message.automation_id == a.id, Message.record_id == rec.id, Message.status.in_(["pending", "generated", "approved", "sent"]))
                    .first()
                )
                if existing:
                    continue
                msg = Message(
                    automation_id=a.id,
                    record_id=rec.id,
                    channel=a.channel,
                    status="pending",
                    scheduled_for=scheduled_dt,
                )
                db.add(msg)
                created += 1
        db.commit()
        return created
    finally:
        db.close()


def generate_pending_messages() -> int:
    """Generate content for pending messages using AI + template"""
    db: Session = SessionLocal()
    try:
        pending = db.query(Message).filter(Message.status == "pending").limit(100).all()
        ai = AIService()
        generated = 0
        for m in pending:
            a = db.get(Automation, m.automation_id) if m.automation_id else None
            tpl = db.get(Template, a.template_id) if a else None
            rec = db.query(Message).get(m.record_id)  # FIXME: should be DatasetRecord
            if not tpl or not rec:
                m.status = "failed"
                db.add(m)
                continue
            # Simple hydration: replace {{key}} with rec.data[key]
            from app.db.models.dataset_record import DatasetRecord
            rec_obj = db.get(DatasetRecord, m.record_id)
            if not rec_obj:
                m.status = "failed"
                db.add(m)
                continue
            prompt = tpl.content
            for k, v in rec_obj.data.items():
                prompt = prompt.replace("{{" + k + "}}", str(v))
            body = ai.generate_message(prompt)
            m.body = body
            m.subject = tpl.name if m.channel == "email" else None
            m.status = "generated"
            db.add(m)
            generated += 1
        db.commit()
        return generated
    finally:
        db.close()


def auto_approve_messages() -> int:
    """Auto-approve messages from automations in auto mode"""
    db: Session = SessionLocal()
    try:
        msgs = db.query(Message).filter(Message.status == "generated").all()
        approved = 0
        for m in msgs:
            a = db.get(Automation, m.automation_id) if m.automation_id else None
            if a and a.mode == "auto":
                m.status = "approved"
                db.add(m)
                approved += 1
        db.commit()
        return approved
    finally:
        db.close()


def send_approved_messages() -> int:
    """Send approved messages via providers"""
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        approved = db.query(Message).filter(Message.status == "approved", Message.scheduled_for <= now).all()
        sms = SMSProvider()
        email = EmailProvider()
        sent = 0
        for m in approved:
            from app.db.models.dataset_record import DatasetRecord
            rec = db.get(DatasetRecord, m.record_id)
            if not rec:
                m.status = "failed"
                db.add(m)
                continue
            # Infer contact from record data
            contact_email = rec.data.get("email") or rec.data.get("Email")
            contact_phone = rec.data.get("phone") or rec.data.get("Phone")
            ok = False
            if m.channel == "sms" and contact_phone:
                ok = sms.send_sms(contact_phone, m.body or "")
            elif m.channel == "email" and contact_email:
                ok = email.send_email(contact_email, subject=m.subject or "HeyDay", html=m.body or "")
            m.status = "sent" if ok else "failed"
            db.add(m)
            sent += 1
        db.commit()
        return sent
    finally:
        db.close()

