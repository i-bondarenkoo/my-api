from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app import crud
from app.schemas.user import CreateUser

router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/users", response_class=HTMLResponse)
async def users_list(
    request: Request,
    start: int = 0,
    stop: int = 5,
    session: AsyncSession = Depends(get_db_session),
):
    users_list = await crud.get_list_users_crud(
        start=start,
        stop=stop,
        session=session,
    )
    step = stop - start
    return templates.TemplateResponse(
        request=request,
        name="users_list.html",
        context={
            "users": users_list,
            "start": start,
            "stop": stop,
            "step": step,
        },
    )


@router.get("/", response_class=HTMLResponse)
async def hello_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={},
    )


@router.get("/tasks", response_class=HTMLResponse)
async def tasks_list(
    request: Request,
    start: int = 0,
    stop: int = 5,
    session: AsyncSession = Depends(get_db_session),
):
    tasks_list = await crud.get_list_task_crud(start=start, stop=stop, session=session)
    step = stop - start
    return templates.TemplateResponse(
        request=request,
        name="tasks_list.html",
        context={
            "tasks": tasks_list,
            "start": start,
            "stop": stop,
            "step": step,
        },
    )


@router.get("/projects", response_class=HTMLResponse)
async def projects_list(
    request: Request,
    start: int = 0,
    stop: int = 5,
    session: AsyncSession = Depends(get_db_session),
):
    projects_list = await crud.get_list_projects_crud(
        start=start, stop=stop, session=session
    )
    step = stop - start
    return templates.TemplateResponse(
        request=request,
        name="projects_list.html",
        context={
            "projects": projects_list,
            "start": start,
            "stop": stop,
            "step": step,
        },
    )


@router.post("/users/create-user", response_class=HTMLResponse)
async def make_new_user(
    request: Request,
    user_data: CreateUser,
    session: AsyncSession = Depends(get_db_session),
):
    new_user = await crud.create_user_crud(user=user_data, session=session)
    return templates.TemplateResponse(
        request=request,
        name="create_user.html",
        context={},
    )
