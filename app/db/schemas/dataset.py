from pydantic import BaseModel


class DatasetBase(BaseModel):
    name: str
    description: str | None = None


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class DatasetOut(DatasetBase):
    id: int

    class Config:
        from_attributes = True

