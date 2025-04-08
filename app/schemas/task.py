from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    title: str
    description: str
    status: str
    user_id: int
    project_id: int


class ResponseTaskWithOutID(BaseModel):
    title: str
    description: str
    status: str
    user_id: int
    project_id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseTask(CreateTask):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PartialUpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    user_id: int | None = None
    project_id: int | None = None
