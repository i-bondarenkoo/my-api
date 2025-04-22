import pytest
import pytest_asyncio
import asyncio
from app.models.base import Base
from tests.test_database import get_testdb_session
from app.schemas.user import CreateUser
from app.schemas.task import CreateTask
from app.schemas.project import CreateProject
from app import crud


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# фикстура с сессией
@pytest_asyncio.fixture(scope="function")
async def session_test_db():
    async for session in get_testdb_session():
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# фикстура с тестовыми данными
@pytest_asyncio.fixture(scope="function")
def make_user_data():
    user_data = CreateUser(
        first_name="John",
        last_name="Johns",
        email="john@mail.ru",
    )
    return user_data


@pytest_asyncio.fixture(scope="function")
def make_project_data():
    project_data = CreateProject(
        title="Тестовый проект",
        description="Описание",
        status="в работе",
    )
    return project_data


@pytest_asyncio.fixture(scope="function")
def make_task_data():
    task_data = CreateTask(
        title="Тестовая Задача",
        description="Какое-то описание",
        status="в работе",
        user_id=1,
        project_id=1,
    )
    return task_data


# очистка бд перед каждым тестом
@pytest_asyncio.fixture(autouse=True)
async def clean_db(session_test_db):
    for table in reversed(Base.metadata.sorted_tables):
        await session_test_db.execute(table.delete())
    await session_test_db.commit()


@pytest_asyncio.fixture(scope="function")
async def create_project(make_project_data, session_test_db):
    project = await crud.create_project_crud(
        project_in=make_project_data,
        session=session_test_db,
    )
    return project


@pytest_asyncio.fixture(scope="function")
async def create_user(make_user_data, session_test_db):
    user = await crud.create_user_crud(
        user_in=make_user_data,
        session=session_test_db,
    )
    return user


@pytest_asyncio.fixture(scope="function")
async def create_task(make_task_data, session_test_db):
    task = await crud.create_task_crud(
        task=make_task_data,
        session=session_test_db,
    )
