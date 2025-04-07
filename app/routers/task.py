from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.task import CreateTask, ResponseTask, PartialUpdateTask
from fastapi import APIRouter, Depends
from fastapi import Body, Path, Query
from typing import Annotated
from app import crud
from app.exceptions import (
    USER_NOT_FOUND_EXCEPTION,
    TASK_NOT_FOUND,
    ERROR_PAGINATION,
    NO_DATA_FOR_UPDATES,
    PROJECT_NOT_FOUND_EXCEPTION,
)
from app.crud.task import get_task_by_id_crud
from app.crud.user import get_user_by_id
from app.crud.project import get_project_by_id_crud

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("/", response_model=ResponseTask)
async def create_task(
    task: Annotated[
        CreateTask, Body(description="Поля задачи для создания объекта в БД")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    check_user = await get_user_by_id(task.user_id, session)
    if not check_user:
        raise USER_NOT_FOUND_EXCEPTION
    check_project = await get_project_by_id_crud(task.project_id, session)
    if not check_project:
        raise PROJECT_NOT_FOUND_EXCEPTION
    return await crud.create_task_crud(task=task, session=session)


@router.get("/{task_id}", response_model=ResponseTask)
async def get_task_by_id(
    task_id: Annotated[
        int,
        Path(gt=0, description="ID задачи из БД, информацию о которой нужно вывести"),
    ],
    session: AsyncSession = Depends(get_db_session),
):
    task = await crud.get_task_by_id_crud(task_id, session)
    if not task:
        raise TASK_NOT_FOUND
    return task


@router.get("/", response_model=list[ResponseTask])
async def get_list_task(
    session: AsyncSession = Depends(get_db_session),
    start: int = Query(0, ge=0, description="Начальный индекс списка задач"),
    stop: int = Query(3, gt=0, description="Конечный индекс списка задач"),
):
    if start > stop:
        raise ERROR_PAGINATION
    return await crud.get_list_task_crud(session=session, start=start, stop=stop)


@router.patch("/{task_id}", response_model=ResponseTask)
async def update_task(
    task: Annotated[
        PartialUpdateTask,
        Body(description="Укажите информацию, которую нужно обновить"),
    ],
    task_id: Annotated[int, Path(description="ID задачи, которую нужно обновить")],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.update_task_partial_crud(
        task=task, task_id=task_id, session=session
    )


@router.delete("/{task_id}")
async def delete_task(
    task_id: Annotated[int, Path(description="ID задачи, которую нужно удалить")],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.delete_task_crud(task_id, session)
