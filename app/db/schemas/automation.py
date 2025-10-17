from pydantic import BaseModel


class AutomationBase(BaseModel):
    name: str
    dataset_id: int
    event_type_id: int
    template_id: int
    trigger_column_name: str
    day_offset: int = 0
    send_time: str = "09:00"  # HH:MM
    channel: str = "sms"
    mode: str = "preview"  # preview|auto
    active: bool = False


class AutomationCreate(AutomationBase):
    pass


class AutomationUpdate(BaseModel):
    name: str | None = None
    dataset_id: int | None = None
    event_type_id: int | None = None
    template_id: int | None = None
    trigger_column_name: str | None = None
    day_offset: int | None = None
    send_time: str | None = None
    channel: str | None = None
    mode: str | None = None
    active: bool | None = None


class AutomationOut(AutomationBase):
    id: int

    class Config:
        from_attributes = True

