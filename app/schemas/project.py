from pydantic import BaseModel, ConfigDict


class CreateProject(BaseModel):
    title: str
    description: str | None = None
    status: str


class ResponseProject(CreateProject):
    id: int

    model_config = ConfigDict(from_attributes=True)
