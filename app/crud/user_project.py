from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_id
from app.crud.project import get_project_by_id_crud
from app.exceptions import USER_NOT_FOUND_EXCEPTION, PROJECT_NOT_FOUND_EXCEPTION
from app.models import secondary_table
from sqlalchemy import insert
from fastapi import HTTPException
from app.models.user import UserOrm
from app.models.project import ProjectOrm
from sqlalchemy import select


# добавление записи в сводную таблицу
async def insert_secondary_table_crud(
    user_id: int, project_id: int, session: AsyncSession
):
    user = await get_user_by_id(user_id, session)
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    project = await get_project_by_id_crud(project_id, session)
    if not project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    stmt = insert(secondary_table).values(user_id=user_id, project_id=project_id)

    try:
        await session.execute(stmt)
        await session.commit()
        # await session.flush()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Такая запись уже существует",
        )

    return {"message": "Данные добавлены"}


async def get_list_users_for_project_crud(project_id: int, session: AsyncSession):
    project = await get_project_by_id_crud(project_id, session)
    if not project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    stmt = (
        select(UserOrm)
        .join(secondary_table, secondary_table.c.user_id == UserOrm.id)
        .where(secondary_table.c.project_id == project_id)
    )
    result = await session.execute(stmt)
    list_users = result.scalars().all()
    return list_users


async def get_list_projects_for_user_crud(user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    stmt = (
        select(ProjectOrm)
        .join(secondary_table, secondary_table.c.project_id == ProjectOrm.id)
        .where(secondary_table.c.user_id == user_id)
    )
    result = await session.execute(stmt)
    list_projects = result.scalars().all()
    return list_projects
