from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import ResponseUser
    from app.schemas.project import ResponseProjectWithOutID


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


class ResponseTaskWithUserInfo(BaseModel):
    title: str
    description: str
    status: str
    user: "ResponseUser"
    model_config = ConfigDict(from_attributes=True)


class ResponseTaskWithProjectInfo(BaseModel):
    title: str
    description: str
    status: str
    project: "ResponseProjectWithOutID"
    model_config = ConfigDict(from_attributes=True)


class ResponseTaskInfo(BaseModel):
    id: int
    title: str
    description: str
    status: str
    user_id: int
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
