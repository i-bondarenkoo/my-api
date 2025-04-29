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


@router.get("/users", response_class=HTMLResponse)
async def users_list(
    request: Request,
    start: int,
    stop: int,
    session: AsyncSession = Depends(get_db_session),
):
    users_list = await crud.get_list_users_crud(
        start=start,
        stop=stop,
        session=session,
    )
    return templates.TemplateResponse(
        request=request, name="users_list.html", context={"users": users_list}
    )
