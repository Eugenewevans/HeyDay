from pydantic import BaseModel


class DatasetSchemaBase(BaseModel):
    dataset_id: int
    column_name: str
    semantic_role: str | None = None
    is_trigger_candidate: bool = False


class DatasetSchemaCreate(DatasetSchemaBase):
    pass


class DatasetSchemaUpdate(BaseModel):
    semantic_role: str | None = None
    is_trigger_candidate: bool | None = None


class DatasetSchemaOut(DatasetSchemaBase):
    id: int

    class Config:
        from_attributes = True

