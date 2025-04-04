from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import Table, Column, ForeignKey

secondary_table = Table(
    "project_users",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
)
