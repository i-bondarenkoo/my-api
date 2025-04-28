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


# @router.get("/users/{user_id}", response_class=HTMLResponse)
# async def read_user(
#     request: Request, user_id: int, session: AsyncSession = Depends(get_db_session)
# ):
#     user = await crud.get_user_by_id(user_id, session)
#     return templates.TemplateResponse(
#         request=request, name="home.html", context={"request": request, "user": user}
#     )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
