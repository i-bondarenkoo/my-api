import pytest
from app.schemas.user import ResponseUser, PatchUpdateUser, CreateUser
from app import crud
from app.models.user import UserOrm
from sqlalchemy import select
import random
import string
from fastapi import HTTPException, status


def generate_rand_email():
    lenght = 7
    rand_str = "".join(random.choices(string.ascii_letters, k=lenght))
    return f"{rand_str}@mail.ru"


def user_data_2():
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
async def test_create_user(
    create_user,
    session_test_db,
    make_user_data,
):
    assert create_user is not None
    assert create_user.first_name == make_user_data.first_name
    assert create_user.last_name == make_user_data.last_name
    assert create_user.email == make_user_data.email
    assert isinstance(create_user.id, int)
    stmt = await session_test_db.execute(
        select(UserOrm).where(UserOrm.id == create_user.id)
    )
    user_in_db = stmt.scalars().first()
    assert user_in_db is not None
    assert user_in_db.first_name == create_user.first_name
    assert user_in_db.last_name == create_user.last_name
    assert user_in_db.email == create_user.email


@pytest.mark.asyncio
async def test_get_users_by_id(
    create_user,
    session_test_db,
):
    response = await crud.get_user_by_id(
        user_id=create_user.id, session=session_test_db
    )
    assert response is not None
    assert isinstance(response.id, int)
    assert response.first_name == create_user.first_name
    assert response.last_name == create_user.last_name
    assert response.email == create_user.email


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
async def test_get_list_users(
    session_test_db,
    start,
    stop,
    expected_len,
):
    for _ in range(5):
        await crud.create_user_crud(
            user_in=user_data_2(),
            session=session_test_db,
        )
    response = await crud.get_list_users_crud(
        session=session_test_db,
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
    session_test_db,
    create_user,
    first_name,
    last_name,
    email,
):
    # Создаем объект для частичного обновления
    update_user = PatchUpdateUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    # Выполняем обновление
    response = await crud.update_user_patch_crud(
        user=update_user, user_id=create_user.id, session=session_test_db
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
async def test_delete_user(
    create_user,
    session_test_db,
):

    response = await crud.delete_user_crud(
        user_id=create_user.id,
        session=session_test_db,
    )
    assert response == {
        "message": "Пользователь успешно удален",
    }
    stmt = await session_test_db.execute(
        select(UserOrm).where(UserOrm.id == create_user.id)
    )
    check_user = stmt.scalars().first()
    assert check_user is None


@pytest.mark.asyncio
async def test_delete_fake_user(
    session_test_db,
):
    # обработка ошибки
    with pytest.raises(HTTPException) as e:
        await crud.delete_user_crud(
            user_id=111,
            session=session_test_db,
        )
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert e.value.detail == "Пользователь не найден"


@pytest.mark.asyncio
async def test_get_user_with_task_and_project(
    session_test_db,
    make_task_data,
    create_user,
    create_project,
):
    update_task_data = make_task_data.model_copy(
        update={
            "user_id": create_user.id,
            "project_id": create_project.id,
        }
    )
    new_task = await crud.create_task_crud(
        task=update_task_data,
        session=session_test_db,
    )
    await crud.insert_secondary_table_crud(
        user_id=create_user.id,
        project_id=create_project.id,
        session=session_test_db,
    )
    result = await crud.get_user_with_projects_and_tasks_crud(
        user_id=create_user.id,
        session=session_test_db,
    )
    assert result is not None
    assert len(result.tasks) == 1
    assert len(result.projects) == 1
    assert result.tasks[0].title == "Тестовая Задача"
    assert result.tasks[0].description == "Какое-то описание"
    assert result.projects[0].title == "Тестовый проект"
    assert result.projects[0].description == "Описание"


@pytest.mark.asyncio
async def test_get_user_with_project(
    create_user,
    create_project,
    session_test_db,
):
    await crud.insert_secondary_table_crud(
        user_id=create_user.id,
        project_id=create_project.id,
        session=session_test_db,
    )
    result = await crud.get_user_with_projects(
        user_id=create_user.id,
        session=session_test_db,
    )
    assert result is not None
    assert len(result.projects) == 1
    assert result.projects[0].title == "Тестовый проект"
    assert result.projects[0].description == "Описание"
