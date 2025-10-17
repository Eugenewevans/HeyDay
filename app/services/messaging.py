from typing import Optional
import httpx

from app.core.config import settings


class SMSProvider:
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None, from_number: Optional[str] = None) -> None:
        self.account_sid = account_sid or settings.twilio_account_sid
        self.auth_token = auth_token or settings.twilio_auth_token
        self.from_number = from_number or settings.twilio_from_number

    def send_sms(self, to: str, body: str) -> bool:
        if not (self.account_sid and self.auth_token and self.from_number):
            return True  # Dev mode
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
            resp = httpx.post(
                url,
                auth=(self.account_sid, self.auth_token),
                data={"From": self.from_number, "To": to, "Body": body + "\n\nReply STOP to unsubscribe."},
                timeout=10,
            )
            return resp.status_code in (200, 201)
        except Exception:
            return False


class EmailProvider:
    def __init__(self, api_key: Optional[str] = None, from_email: Optional[str] = None) -> None:
        self.api_key = api_key or settings.sendgrid_api_key
        self.from_email = from_email or settings.sendgrid_from_email

    def send_email(self, to: str, subject: str, html: str) -> bool:
        if not (self.api_key and self.from_email):
            return True  # Dev mode
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            payload = {
                "personalizations": [{"to": [{"email": to}]}],
                "from": {"email": self.from_email},
                "subject": subject,
                "content": [{"type": "text/html", "value": html}],
            }
            resp = httpx.post(url, json=payload, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=10)
            return resp.status_code in (200, 202)
        except Exception:
            return False

