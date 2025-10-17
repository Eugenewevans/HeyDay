from pydantic import BaseModel


class DatasetFieldMapBase(BaseModel):
    dataset_id: int
    role: str  # name|email|phone|trigger_date
    source_column: str


class DatasetFieldMapCreate(DatasetFieldMapBase):
    pass


class DatasetFieldMapUpdate(BaseModel):
    source_column: str


class DatasetFieldMapOut(DatasetFieldMapBase):
    id: int

    class Config:
        from_attributes = True

