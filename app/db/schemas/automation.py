from pydantic import BaseModel


class AutomationBase(BaseModel):
    name: str
    dataset_id: int
    event_type_id: int
    template_id: int
    day_offset: int = 0
    send_time: str = "09:00"  # HH:MM
    channel: str = "sms"
    active: bool = False


class AutomationCreate(AutomationBase):
    pass


class AutomationUpdate(BaseModel):
    name: str | None = None
    dataset_id: int | None = None
    event_type_id: int | None = None
    template_id: int | None = None
    day_offset: int | None = None
    send_time: str | None = None
    channel: str | None = None
    active: bool | None = None


class AutomationOut(AutomationBase):
    id: int

    class Config:
        from_attributes = True

