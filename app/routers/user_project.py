from fastapi import APIRouter, Query, Depends
from app.core.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app import crud

router = APIRouter(
    prefix="/user-project",
    tags=["Secondary Table"],
)


@router.post("/add")
async def insert_data(
    user_id: Annotated[int, Query(description="ID пользователя")],
    project_id: Annotated[int, Query(description="ID проекта")],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.insert_secondary_table_crud(
        user_id=user_id, project_id=project_id, session=session
    )


@router.get("/info-user")
async def get_list_users_for_project(
    project_id: Annotated[int, Query()],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.get_list_users_for_project_crud(
        project_id=project_id, session=session
    )


@router.get("/info-project")
async def get_list_projects_for_user(
    user_id: Annotated[
        int,
        Query(),
    ],
    session: AsyncSession = Depends(get_db_session),
):
    return await crud.get_list_projects_for_user_crud(user_id=user_id, session=session)
