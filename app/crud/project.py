from app.schemas.project import CreateProject
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import ProjectOrm
from sqlalchemy import select


async def create_project_crud(project_in: CreateProject, session: AsyncSession):
    new_project = ProjectOrm(**project_in.model_dump())
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    return new_project


async def get_project_by_id_crud(project_id: int, session: AsyncSession):
    current_project = await session.get(ProjectOrm, project_id)
    return current_project


async def get_list_projects_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(ProjectOrm).order_by(ProjectOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    return result.scalars().all()
