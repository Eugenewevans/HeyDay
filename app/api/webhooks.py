"""Phase 7: SMS STOP handler webhook"""
from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session

from app.db.models.consent import Consent
from app.db.session import get_db


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/sms-status")
def twilio_sms_webhook(Body: str = Form(...), From: str = Form(...), db: Session = Depends(get_db)):
    """Handle Twilio SMS status callbacks and STOP commands"""
    body_lower = Body.strip().lower()
    if body_lower in ("stop", "unsubscribe", "cancel", "end", "quit"):
        # Mark opt-out
        consent = db.query(Consent).filter(Consent.customer_id == From, Consent.channel == "sms").first()
        if consent:
            consent.status = "opt_out"
            db.add(consent)
        else:
            # FIXME: need to resolve phone→customer_id; for now skip
            pass
        db.commit()
    return {"status": "ok"}

