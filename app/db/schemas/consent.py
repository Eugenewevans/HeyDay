from pydantic import BaseModel


class ConsentBase(BaseModel):
    customer_id: int
    channel: str  # sms|email
    status: str = "opt_in"  # opt_in|opt_out
    source: str | None = None


class ConsentCreate(ConsentBase):
    pass


class ConsentUpdate(BaseModel):
    status: str | None = None
    source: str | None = None


class ConsentOut(ConsentBase):
    id: int

    class Config:
        from_attributes = True

