import pytest

import pytest_asyncio

from tests.test_database import get_testdb_sesion
from app.schemas.user import CreateUser
from app import crud
from app.models.user import UserOrm
from sqlalchemy import select


# фикстура с сессией
@pytest_asyncio.fixture(scope="function")
async def get_session_test_db():
    async for session in get_testdb_sesion():
        async with session.begin_nested():
            yield session
        await session.rollback()


# фикстура с тестовыми данными
@pytest_asyncio.fixture(scope="function")
def get_user_data():
    user_data = CreateUser(
        first_name="John",
        last_name="Johns",
        email="john@mail.ru",
    )
    return user_data


@pytest.mark.asyncio
async def test_create_user(get_session_test_db, get_user_data):
    response = await crud.create_user_crud(
        user_in=get_user_data, session=get_session_test_db
    )
    assert response is not None
    assert response.first_name == "John"
    assert response.last_name == "Johns"
    assert response.email == "john@mail.ru"
    assert isinstance(response.id, int)
    stmt = await get_session_test_db.execute(
        select(UserOrm).where(UserOrm.id == response.id)
    )
    user_in_db = stmt.scalars().first()
    assert user_in_db is not None
    assert user_in_db.first_name == response.first_name
    assert user_in_db.last_name == response.last_name
    assert user_in_db.email == response.email


@pytest.mark.asyncio
async def test_get_users_by_id(get_session_test_db, get_user_data):
    # создаю пользователя
    user = await crud.create_user_crud(
        user_in=get_user_data,
        session=get_session_test_db,
    )
    response = await crud.get_user_by_id(user_id=user.id, session=get_session_test_db)
    assert response is not None
    assert isinstance(response.id, int)
    assert response.first_name == "John"
    assert response.last_name == "Johns"
    assert response.email == "john@mail.ru"
