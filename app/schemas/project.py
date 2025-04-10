from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import ResponseUser
    from app.schemas.task import ResponseTaskInfo


class CreateProject(BaseModel):
    title: str
    description: str | None = None
    status: str


class ResponseProjectWithOutID(BaseModel):
    title: str
    description: str | None = None
    status: str
    model_config = ConfigDict(from_attributes=True)


class ResponseProject(CreateProject):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseProjectWithUsersInfo(ResponseProjectWithOutID):
    users: list["ResponseUser"]


class ResponseProjectWithTasksInfo(ResponseProjectWithOutID):
    tasks: list["ResponseTaskInfo"]


class PatchUpdateProject(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
