from pydantic import BaseModel


class EventTypeBase(BaseModel):
    key: str
    name: str


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeUpdate(BaseModel):
    key: str | None = None
    name: str | None = None


class EventTypeOut(EventTypeBase):
    id: int

    class Config:
        from_attributes = True

