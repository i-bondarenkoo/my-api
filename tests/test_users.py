import pytest
import pytest_asyncio
import asyncio
from app.models.base import Base
from tests.test_database import get_testdb_session
from app.schemas.user import ResponseUser, PatchUpdateUser, CreateUser, ResponseUserInfo
from app import crud
from app.models.user import UserOrm
from sqlalchemy import select
import random
import string
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload


def generate_rand_email():
    lenght = 7
    rand_str = "".join(random.choices(string.ascii_letters, k=lenght))
    return f"{rand_str}@mail.ru"


def get_user_data_2():
    user_data_2 = CreateUser(
        first_name="Andy",
        last_name="Orton",
        email=generate_rand_email(),
    )
    return user_data_2


def update_user():
    update_data = PatchUpdateUser(
        first_name="Test",
        # email='test@mail.ru',
    )
    return update_data


@pytest.mark.asyncio
async def test_create_user(get_session_test_db, get_user_data):
    response = await crud.create_user_crud(
        user_in=get_user_data, session=get_session_test_db
    )
    assert response is not None
    assert response.first_name == get_user_data.first_name
    assert response.last_name == get_user_data.last_name
    assert response.email == get_user_data.email
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
    assert response.first_name == get_user_data.first_name
    assert response.last_name == get_user_data.last_name
    assert response.email == get_user_data.email


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "start, stop, expected_len",
    [
        (0, 0, 0),
        (0, 1, 1),
        (1, 4, 3),
        (3, 5, 2),
        (5, 10, 0),
    ],
)
async def test_get_list_users(get_session_test_db, start, stop, expected_len):
    for _ in range(5):
        await crud.create_user_crud(
            user_in=get_user_data_2(),
            session=get_session_test_db,
        )
    response = await crud.get_list_users_crud(
        session=get_session_test_db,
        start=start,
        stop=stop,
    )
    assert response is not None
    assert len(response) == expected_len
    assert isinstance(response, list)
    if response:
        assert isinstance(response[0], UserOrm)
        response_user = ResponseUser.model_validate(response[0])
        assert isinstance(response_user, ResponseUser)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "first_name, last_name, email",
    [
        (None, None, None),
        ("John", None, None),
        ("John", "Karlson", None),
        ("John", "Karlson", "john-karlson@mail.ru"),
        (None, "Karlson", "john-karlson@mail.ru"),
        (None, None, "john-karlson@mail.ru"),
        (None, "Karlson", None),
        ("John", None, "john-karlson@mail.ru"),
    ],
)
async def test_update_user(
    get_session_test_db, get_user_data, first_name, last_name, email
):
    user = await crud.create_user_crud(
        user_in=get_user_data,
        session=get_session_test_db,
    )
    # Создаем объект для частичного обновления
    update_user = PatchUpdateUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    # Выполняем обновление
    response = await crud.update_user_patch_crud(
        user=update_user, user_id=user.id, session=get_session_test_db
    )
    assert response is not None
    # Проверяем, что только те поля, которые переданы, были обновлены
    if first_name is not None:
        assert response.first_name == first_name
    if last_name is not None:
        assert response.last_name == last_name
    if email is not None:
        assert response.email == email


@pytest.mark.asyncio
async def test_delete_user(get_session_test_db, get_user_data):
    user = await crud.create_user_crud(
        user_in=get_user_data,
        session=get_session_test_db,
    )

    response = await crud.delete_user_crud(
        user_id=user.id,
        session=get_session_test_db,
    )
    assert response == {
        "message": "Пользователь успешно удален",
    }
    stmt = await get_session_test_db.execute(
        select(UserOrm).where(UserOrm.id == user.id)
    )
    check_user = stmt.scalars().first()
    assert check_user is None


@pytest.mark.asyncio
async def test_delete_fake_user(get_session_test_db):
    # обработка ошибки
    with pytest.raises(HTTPException) as e:
        await crud.delete_user_crud(
            user_id=111,
            session=get_session_test_db,
        )
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert e.value.detail == "Пользователь не найден"


@pytest.mark.asyncio
async def test_get_user_with_task_and_project(
    get_session_test_db,
    get_task_data,
    get_project_data,
    get_user_data,
):
    user = await crud.create_user_crud(
        user_in=get_user_data,
        session=get_session_test_db,
    )
    project = await crud.create_project_crud(
        project_in=get_project_data,
        session=get_session_test_db,
    )

    task = await crud.create_task_crud(
        task=get_task_data,
        session=get_session_test_db,
    )
    stmt = await get_session_test_db.execute(
        select(UserOrm)
        .where(UserOrm.id == user.id)
        .options(
            selectinload(UserOrm.tasks),
            selectinload(UserOrm.projects),
        )
    )
    check_user = stmt.scalars().first()
    assert check_user is not None
    validate_user = ResponseUserInfo.model_validate(check_user)
    assert isinstance(validate_user, ResponseUserInfo)
