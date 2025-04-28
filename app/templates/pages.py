from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app import crud


router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(
    request: Request, user_id: int, session: AsyncSession = Depends(get_db_session)
):
    user = await crud.get_user_by_id(user_id, session)
    return templates.TemplateResponse(
        request=request, name="home.html", context={"request": request, "user": user}
    )


@router.get("/tasks/{task_id}", response_class=HTMLResponse)
async def read_task(
    request: Request,
    task_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    task = await crud.get_task_by_id_crud(task_id, session)
    return templates.TemplateResponse(
        request=Request,
        name="task_detail.html",
        context={"request": request, "task": task},
    )
