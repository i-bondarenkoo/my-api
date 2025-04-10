from app.schemas.project import (
    CreateProject,
    ResponseProject,
    PatchUpdateProject,
    ResponseProjectWithUsersInfo,
    ResponseProjectWithTasksInfo,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, Body, Path, Query
from app.core.database import get_db_session
from app import crud
from typing import Annotated
from app.exceptions import (
    PROJECT_NOT_FOUND_EXCEPTION,
    LIST_PROJECTS_NOT_FOUND_EXCEPTION,
    ERROR_PAGINATION,
)

router = APIRouter(
    prefix="/projects",
    tags=["Project"],
)


@router.post("/", response_model=ResponseProject)
async def create_project(
    project_in: Annotated[
        CreateProject, Body(description="Поле сущности для создания объекта в БД")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.create_project_crud(project_in=project_in, session=session)


@router.get("/", response_model=list[ResponseProject])
async def get_list_projects(
    session: AsyncSession = Depends(get_db_session),
    start: int = Query(0, ge=0, description="Начальный индекс список"),
    stop: int = Query(3, gt=0, description="Укажите конечный индекс списка"),
):
    if start > stop:
        raise ERROR_PAGINATION
    list_projects = await crud.get_list_projects_crud(session, start, stop)
    if not list_projects:
        raise LIST_PROJECTS_NOT_FOUND_EXCEPTION
    return list_projects


@router.get("/{project_id}", response_model=ResponseProject)
async def get_project_by_id(
    project_id: Annotated[
        int, Path(gt=0, description="ID проекта, информацию о котором нужно получить")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    project = await crud.get_project_by_id_crud(project_id, session)
    if not project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    return project


@router.get("/{project_id}/users", response_model=ResponseProjectWithUsersInfo)
async def get_users_in_project(
    project_id: Annotated[
        int, Path(gt=0, description="ID проекта, для  получения списка участников")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.get_users_in_project_crud(project_id=project_id, session=session)


@router.get("/{project_id}/tasks", response_model=ResponseProjectWithTasksInfo)
async def get_tasks_in_project(
    project_id: Annotated[
        int, Path(gt=0, description="ID проекта, для просмотра списка участников")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.get_tasks_in_project_crud(project_id=project_id, session=session)


@router.patch("/{project_id}", response_model=ResponseProject)
async def update_project(
    project: Annotated[
        PatchUpdateProject,
        Body(
            description="Колонки таблицы, в которых нужно обновить информацию о проекте"
        ),
    ],
    project_id: Annotated[
        int, Path(description="ID проекта, в котором нужно внести изменения")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.update_project_patch_crud(
        project=project, project_id=project_id, session=session
    )


@router.delete("/{project_id}")
async def delete_project(
    project_id: Annotated[int, Path(description="ID проекта, который удаляем")],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.delete_project_crud(project_id=project_id, session=session)
