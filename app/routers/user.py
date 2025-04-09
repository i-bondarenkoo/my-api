from fastapi import APIRouter, Depends, Path, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.exceptions import (
    USER_NOT_FOUND_EXCEPTION,
    LIST_NOT_FOUND_EXCEPTION,
    ERROR_PAGINATION,
)
from app.schemas.user import (
    CreateUser,
    ResponseUser,
    PatchUpdateUser,
    ResponseUserInfo,
    ResponseUserWithProjects,
)
from app import crud
from typing import Annotated
from app.exceptions import USER_NOT_FOUND_EXCEPTION

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=ResponseUser)
async def create_user(
    user_in: Annotated[
        CreateUser, Body(description="Поля пользователя для создания объекта в БД")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.create_user_crud(user_in=user_in, session=session)


@router.get("/{user_id}", response_model=ResponseUser)
async def get_user_by_id(
    user_id: Annotated[
        int,
        Path(
            gt=0, description="Введите ID пользователя, для получения информации о нем"
        ),
    ],
    session: AsyncSession = Depends(get_db_session),
):
    user = await crud.get_user_by_id(user_id, session)
    if user is None:
        raise USER_NOT_FOUND_EXCEPTION
    return user


@router.get("/", response_model=list[ResponseUser])
async def get_list_users(
    session: AsyncSession = Depends(get_db_session),
    start: int = Query(0, ge=0, description="Начальный индекс списка пользователей"),
    stop: int = Query(3, gt=0, description="Конечный индекс списка пользователей"),
):
    if start > stop:
        raise ERROR_PAGINATION
    return await crud.get_list_users_crud(session=session, start=start, stop=stop)


@router.get("/{user_id}/projects", response_model=ResponseUserWithProjects)
async def get_list_projects_for_user(
    user_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID пользователя для дополнительной информации о его участии в проектах",
        ),
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.get_user_with_projects(user_id=user_id, session=session)


@router.get("/{user_id}/details", response_model=ResponseUserInfo)
async def get_user_with_projects_and_tasks(
    user_id: Annotated[
        int,
        Path(gt=0, description="ID пользователя для получения подробной информации"),
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.get_user_with_projects_and_tasks_crud(
        user_id=user_id, session=session
    )


@router.patch("/{user_id}", response_model=ResponseUser)
async def update_user(
    user: Annotated[
        PatchUpdateUser, Body(description="Укажите информацию которую нужно обновить")
    ],
    user_id: Annotated[
        int, Path(gt=0, description="ID пользователя, которого нужно обновить")
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.update_user_patch_crud(
        user=user,
        user_id=user_id,
        session=session,
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[
        int, Path(gt=0, description="ID Пользователя, которого нужно удалить")
    ],
    session: AsyncSession = Depends(get_db_session),
) -> None:
    return await crud.delete_user_crud(user_id=user_id, session=session)
