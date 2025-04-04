from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import String
from typing import TYPE_CHECKING
from app.models.user_projects import secondary_table

if TYPE_CHECKING:
    from app.models.task import TaskOrm
    from app.models.project import ProjectOrm


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True)

    tasks: Mapped[list["TaskOrm"]] = relationship(
        "TaskOrm",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    projects: Mapped[list["ProjectOrm"]] = relationship(
        "ProjectOrm",
        secondary=secondary_table,
        back_populates="users",
    )
