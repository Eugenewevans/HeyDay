from typing import Optional

from app.core.config import settings


class SMSProvider:
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None, from_number: Optional[str] = None) -> None:
        self.account_sid = account_sid or settings.twilio_account_sid
        self.auth_token = auth_token or settings.twilio_auth_token
        self.from_number = from_number or settings.twilio_from_number

    def send_sms(self, to: str, body: str) -> bool:
        # Placeholder: integrate twilio client here
        if not (self.account_sid and self.auth_token and self.from_number):
            # Dev mode: simulate success
            return True
        # TODO: real Twilio integration
        return True


class EmailProvider:
    def __init__(self, api_key: Optional[str] = None, from_email: Optional[str] = None) -> None:
        self.api_key = api_key or settings.sendgrid_api_key
        self.from_email = from_email or settings.sendgrid_from_email

    def send_email(self, to: str, subject: str, html: str) -> bool:
        # Placeholder: integrate SendGrid client here
        if not (self.api_key and self.from_email):
            # Dev mode: simulate success
            return True
        # TODO: real SendGrid integration
        return True

