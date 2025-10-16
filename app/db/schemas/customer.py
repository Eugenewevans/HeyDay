from datetime import date

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    phone: str | None = None
    email: EmailStr | None = None
    birthday: date | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    birthday: date | None = None


class CustomerOut(CustomerBase):
    id: int

    class Config:
        from_attributes = True

