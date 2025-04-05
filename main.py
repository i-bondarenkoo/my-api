from fastapi import FastAPI
import uvicorn
from app.routers.user import router as user_router
from app.routers.project import router as project_router


app = FastAPI(title="Мое первое API")
app.include_router(user_router)
app.include_router(project_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
