from fastapi import FastAPI
import uvicorn
from app.routers.user import router as user_router
from app.routers.project import router as project_router
from app.routers.task import router as task_router
from app.routers.user_project import router as association_router
from app.auth.authorization import router as auth_router
from app.templates.users.views import router as user_views
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="To-do list API ^_^")
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(association_router)
app.include_router(auth_router)
app.include_router(user_views)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
