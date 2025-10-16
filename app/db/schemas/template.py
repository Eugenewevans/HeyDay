from pydantic import BaseModel


class TemplateBase(BaseModel):
    name: str
    channel: str
    content: str


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: str | None = None
    channel: str | None = None
    content: str | None = None


class TemplateOut(TemplateBase):
    id: int

    class Config:
        from_attributes = True

