from pydantic import BaseModel, ConfigDict, EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.task import ResponseTaskOut
    from app.schemas.project import ResponseProjectOut


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ResponseUser(CreateUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseUserOut(CreateUser):
    model_config = ConfigDict(from_attributes=True)


class PatchUpdateUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class ResponseUserWithTaskAndProject(BaseModel):
    first_name: str
    last_name: str
    email: str
    tasks: list["ResponseTaskOut"]
    projects: list["ResponseProjectOut"]
