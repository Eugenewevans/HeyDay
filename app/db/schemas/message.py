from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    automation_id: int | None = None
    customer_id: int
    channel: str  # sms|email
    status: str = "planned"
    subject: str | None = None
    body: str | None = None
    scheduled_for: datetime | None = None


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    status: str | None = None
    subject: str | None = None
    body: str | None = None
    scheduled_for: datetime | None = None


class MessageOut(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

