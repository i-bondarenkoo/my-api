import pytest
import pytest_asyncio
import asyncio
from app.models.base import Base
from tests.test_database import get_testdb_session
from app.schemas.user import CreateUser


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# фикстура с сессией
@pytest_asyncio.fixture(scope="function")
async def get_session_test_db():
    async for session in get_testdb_session():
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# фикстура с тестовыми данными
@pytest_asyncio.fixture(scope="function")
def get_user_data():
    user_data = CreateUser(
        first_name="John",
        last_name="Johns",
        email="john@mail.ru",
    )
    return user_data


# очистка бд перед каждым тестом
@pytest_asyncio.fixture(autouse=True)
async def clean_db(get_session_test_db):
    for table in reversed(Base.metadata.sorted_tables):
        await get_session_test_db.execute(table.delete())
    await get_session_test_db.commit()
