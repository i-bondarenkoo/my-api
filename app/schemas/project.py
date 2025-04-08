from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.task import ResponseTaskOut
    from app.schemas.user import ResponseUserOut


class CreateProject(BaseModel):
    title: str
    description: str | None = None
    status: str


class ResponseProjectOut(BaseModel):
    title: str
    description: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ResponseProject(CreateProject):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseProjectWithTasksAndUsers(BaseModel):
    title: str
    description: str
    status: str
    tasks: list["ResponseTaskOut"]
    users: list["ResponseUserOut"]


class PatchUpdateProject(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
