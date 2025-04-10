from app.schemas.project import CreateProject, PatchUpdateProject
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import ProjectOrm
from sqlalchemy import select
from app.exceptions import PROJECT_NOT_FOUND_EXCEPTION, NO_DATA_FOR_UPDATES
from sqlalchemy.orm import selectinload


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


async def update_project_patch_crud(
    project: PatchUpdateProject, project_id: int, session: AsyncSession
):
    update_project = await session.get(ProjectOrm, project_id)
    if not update_project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    data = project.model_dump(exclude_unset=True)
    if not data:
        raise NO_DATA_FOR_UPDATES
    for key, value in data.items():
        setattr(update_project, key, value)
    await session.commit()
    await session.refresh(update_project)
    return update_project


async def delete_project_crud(project_id: int, session: AsyncSession):
    project = await get_project_by_id_crud(project_id, session)
    if not project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    await session.delete(project)
    await session.commit()
    return {
        "message": "Проект успешно удален",
    }


# вывести всех участников проекта
async def get_users_in_project_crud(project_id: int, session: AsyncSession):
    current_project = await get_project_by_id_crud(project_id, session)
    if not current_project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    stmt = (
        select(ProjectOrm)
        .where(ProjectOrm.id == project_id)
        .options(
            selectinload(ProjectOrm.users),
        )
    )
    result = await session.execute(stmt)
    return result.scalars().one()


# вывести все задачи в проекте
async def get_tasks_in_project_crud(project_id: int, session: AsyncSession):
    current_project = await get_project_by_id_crud(project_id, session)
    if not current_project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    stmt = (
        select(ProjectOrm)
        .where(ProjectOrm.id == project_id)
        .options(
            selectinload(ProjectOrm.tasks),
        )
    )
    result = await session.execute(stmt)
    return result.scalars().one()
