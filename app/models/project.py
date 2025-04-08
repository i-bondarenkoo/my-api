from app.models.base import Base
from sqlalchemy import Integer, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.user_projects import secondary_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import TaskOrm
    from app.models.user import UserOrm


class ProjectOrm(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(25), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        Date, nullable=False, server_default=func.current_date()
    )

    # 1-n с задачами
    tasks: Mapped["TaskOrm"] = relationship(
        "TaskOrm", back_populates="project", cascade="all, delete-orphan"
    )
    # n-n с пользователями
    users: Mapped[list["UserOrm"]] = relationship(
        "UserOrm", secondary=secondary_table, back_populates="projects"
    )
