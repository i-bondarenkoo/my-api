from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Мое первое API")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
