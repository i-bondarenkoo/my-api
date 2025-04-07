from fastapi import APIRouter, Depends, Path, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.exceptions import (
    USER_NOT_FOUND_EXCEPTION,
    LIST_NOT_FOUND_EXCEPTION,
    ERROR_PAGINATION,
)
from app.schemas.user import CreateUser, ResponseUser, PatchUpdateUser
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
    start: int = Query(0, ge=0, description="Начальный индекс в БД"),
    stop: int = Query(3, gt=0, description="Конечный индекс в БД"),
):
    if start > stop:
        raise ERROR_PAGINATION
    users = await crud.get_list_users_crud(session=session, start=start, stop=stop)
    if not users:
        raise LIST_NOT_FOUND_EXCEPTION
    return users


@router.patch("/{user_id}", response_model=ResponseUser)
async def update_user(
    user: Annotated[
        PatchUpdateUser,
        Body(
            description="Колонки таблицы, в которых нужно изменить информацию о пользователе"
        ),
    ],
    user_id: Annotated[
        int,
        Path(gt=0, description="ID пользователя, информацию о котором хотите изменить"),
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.update_user_patch_crud(
        user=user, user_id=user_id, session=session
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[
        int, Path(gt=0, description="ID Пользователя, которого нужно удалить")
    ],
    session: AsyncSession = Depends(get_db_session),
) -> None:
    return await crud.delete_user_crud(user_id=user_id, session=session)
