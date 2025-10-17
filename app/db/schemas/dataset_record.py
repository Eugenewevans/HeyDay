from pydantic import BaseModel


class DatasetRecordBase(BaseModel):
    dataset_id: int
    data: dict


class DatasetRecordCreate(DatasetRecordBase):
    pass


class DatasetRecordUpdate(BaseModel):
    data: dict


class DatasetRecordOut(DatasetRecordBase):
    id: int

    class Config:
        from_attributes = True

