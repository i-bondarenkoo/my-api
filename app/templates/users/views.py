from fastapi import APIRouter, HTTPException, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app import crud
from app.schemas.user import CreateUser, PatchUpdateUser

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


@router.get("/users/create-user", response_class=HTMLResponse)
async def get_create_user_form(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="create_user.html",
        context={},
    )


@router.post("/users/create-user", response_class=HTMLResponse)
async def make_new_user(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        user_data = CreateUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        new_user = await crud.create_user_crud(user_in=user_data, session=session)
        return templates.TemplateResponse(
            request=request,
            name="create_user.html",
            context={"message": f"Пользователь {new_user.first_name} создан"},
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="create_user.html",
            context={
                "error": "❌ Ошибка при создании пользователя. Проверьте введённые данные."
            },
            status_code=400,
        )


# изменение данных пользователя
@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def get_edit_data_user_form(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    user = await crud.get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return templates.TemplateResponse(
        request=request,
        name="edit_user.html",
        context={"user": user},
    )


@router.post("/users/{user_id}/edit", response_class=HTMLResponse)
async def update_user_form_post(
    request: Request,
    user_id: int,
    first_name: str = Form(None),
    last_name: str = Form(None),
    email: str = Form(None),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        # Создаем словарь только с переданными (не пустыми) значениями
        update_data = {}
        if first_name is not None and first_name != "":
            update_data["first_name"] = first_name
        if last_name is not None and last_name != "":
            update_data["last_name"] = last_name
        if email is not None and email != "":
            update_data["email"] = email

        # Если ничего не передали для обновления
        if not update_data:
            raise ValueError("Не указаны данные для обновления")

        user_data = PatchUpdateUser(**update_data)

        update_user = await crud.update_user_patch_crud(
            user=user_data,
            user_id=user_id,
            session=session,
        )

        return templates.TemplateResponse(
            request=request,
            name="edit_user.html",
            context={
                "user": update_user,
                "message": f"Данные пользователя {update_user.first_name} обновлены",
            },
        )
    except Exception as e:
        user = await crud.get_user_by_id(user_id=user_id, session=session)
        return templates.TemplateResponse(
            request=request,
            name="edit_user.html",
            context={"user": user, "error": f"Ошибка: {str(e)}"},
            status_code=400,
        )


# удаление пользователя
@router.get("/users/{user_id}/delete", response_class=HTMLResponse)
async def get_delete_date_user_form(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    user = await crud.get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return templates.TemplateResponse(
        request=request, name="delete_user.html", context={"user": user}
    )


@router.post("/users/{user_id}/delete", response_class=HTMLResponse)
async def delete_user_form_post(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    user = await crud.get_user_by_id(user_id=user_id, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    await crud.delete_user_crud(user_id=user_id, session=session)
    # Редирект с сообщением об успехе
    return RedirectResponse(
        url="/pages/users?message=Пользователь+удалён", status_code=303
    )
