from pydantic import BaseModel, ConfigDict, EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.task import ResponseTaskWithOutID
    from app.schemas.project import ResponseProjectWithOutID


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseUserWithProjects(BaseModel):
    first_name: str
    last_name: str
    email: str
    projects: list["ResponseProjectWithOutID"]
    model_config = ConfigDict(from_attributes=True)


class ResponseUserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    tasks: list["ResponseTaskWithOutID"]
    projects: list["ResponseProjectWithOutID"]
    model_config = ConfigDict(from_attributes=True)


class PatchUpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserSchemaLogin(BaseModel):
    username: str
    password: str


class UserSchemaResponse(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    model_config = ConfigDict(from_attributes=True)
