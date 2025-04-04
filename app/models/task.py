from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import UserOrm
    from app.models.project import ProjectOrm


class TaskOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    # 1-n с пользователем
    # если в таблицах пользователя или преокта удалят запись, из этой таблицы она тоже удалится
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UserOrm"] = relationship(
        "UserOrm",
        back_populates="tasks",
    )
    # 1-n с проектами
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    project: Mapped["ProjectOrm"] = relationship(
        "ProjectOrm",
        back_populates="tasks",
    )
