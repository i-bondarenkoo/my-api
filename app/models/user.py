from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import String

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import TaskOrm


class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True)

    tasks: Mapped[list["TaskOrm"]] = relationship(
        "TaskOrm",
        back_populates="user",
    )
