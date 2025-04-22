import pytest
from app import crud
from sqlalchemy import select
from app.crud.project import get_users_in_project_crud
from app.schemas.project import ResponseProject, CreateProject, PatchUpdateProject
from app.models.project import ProjectOrm
from app.schemas.task import CreateTask


async def helper_check_project(session, project_id):
    stmt = select(ProjectOrm).where(ProjectOrm.id == project_id)
    result = await session.execute(stmt)
    orm_obj = result.scalars().first()
    assert orm_obj is not None
    assert isinstance(orm_obj, ProjectOrm)
    project_in = ResponseProject.model_validate(orm_obj)
    assert isinstance(project_in, ResponseProject)
    return project_in


@pytest.mark.asyncio
async def test_create_project(create_project, make_project_data, session_test_db):
    assert create_project is not None
    assert create_project.title == make_project_data.title
    assert create_project.description == make_project_data.description
    assert create_project.status == make_project_data.status
    project_in = await helper_check_project(session_test_db, create_project.id)


@pytest.mark.asyncio
async def test_get_project_by_id(create_project, session_test_db):
    response = await crud.get_project_by_id_crud(
        project_id=create_project.id,
        session=session_test_db,
    )
    assert response is not None
    project_in = await helper_check_project(session_test_db, create_project.id)


def generate_projects_list(count: int = 5):
    return [
        CreateProject(
            title=f"Проект {i}",
            description=f"Описание проекта {i}",
            status="в работе",
        )
        for i in range(1, count + 1)
    ]


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
async def test_get_list_project(session_test_db, start, stop, expected_len):
    list_projects = generate_projects_list()
    for project in list_projects:
        await crud.create_project_crud(
            project_in=project,
            session=session_test_db,
        )
    response = await crud.get_list_projects_crud(
        session=session_test_db,
        start=start,
        stop=stop,
    )
    assert response is not None
    assert len(response) == expected_len
    assert isinstance(response, list)
    if response:
        assert isinstance(response[0], ProjectOrm)
        for elem in response:
            response_project = ResponseProject.model_validate(elem)
            assert isinstance(response_project, ResponseProject)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "title, description, status",
    [
        ("Обновленное поле", None, None),
        ("Обновленное поле", "Попытка обновить данные", None),
        ("Обновленное поле", "Попытка обновить данные", "новый статус"),
        (None, "Попытка обновить данные", None),
        (None, "Попытка обновить данные", "новый статус"),
        (None, None, "новый статус"),
        ("Обновленное поле", None, "новый статус"),
        (None, None, None),
    ],
)
async def test_update_project(
    create_project, session_test_db, title, description, status
):
    user_in_db = await helper_check_project(session_test_db, create_project.id)
    update_project = PatchUpdateProject(
        title=title,
        description=description,
        status=status,
    )
    response = await crud.update_project_patch_crud(
        project=update_project,
        project_id=create_project.id,
        session=session_test_db,
    )
    assert response is not None
    if title is not None:
        assert response.title == title
    if description is not None:
        assert response.description == description
    if status is not None:
        assert response.status == status


@pytest.mark.asyncio
async def test_delete_project(create_project, session_test_db):
    await helper_check_project(session_test_db, create_project.id)
    response = await crud.delete_project_crud(
        project_id=create_project.id, session=session_test_db
    )
    assert response == {
        "message": "Проект успешно удален",
    }
    stmt = select(ProjectOrm).where(ProjectOrm.id == create_project.id)
    result = await session_test_db.execute(stmt)
    check_project = result.scalars().first()
    assert check_project is None


@pytest.mark.asyncio
async def test_get_users_in_project(create_user, create_project, session_test_db):
    await crud.insert_secondary_table_crud(
        user_id=create_user.id,
        project_id=create_project.id,
        session=session_test_db,
    )
    response = await get_users_in_project_crud(
        project_id=create_project.id,
        session=session_test_db,
    )
    assert response is not None
    check_query = await crud.get_list_projects_for_user_crud(
        user_id=create_user.id,
        session=session_test_db,
    )
    assert check_query is not None
    assert isinstance(check_query, list)
    assert check_query[0].title == "Тестовый проект"
    assert check_query[0].description == "Описание"
    assert check_query[0].status == "в работе"


@pytest.mark.asyncio
async def test_get_tasks_in_project(create_user, session_test_db):
    projects = []
    for i in range(1, 4):
        project = await crud.create_project_crud(
            project_in=CreateProject(
                title=f"Проект {i}",
                description=f"Описание проекта {i}",
                status="в работе",
            ),
            session=session_test_db,
        )
        projects.append(project)

    for i in range(1, 8):
        await crud.create_task_crud(
            task=CreateTask(
                title=f"Задача {i}",
                description=f"Описание {i}",
                status="в работе",
                user_id=create_user.id,
                project_id=projects[(i - 1) % len(projects)].id,
            ),
            session=session_test_db,
        )
    result_project = await crud.get_tasks_in_project_crud(
        projects[0].id,
        session_test_db,
    )
    assert result_project.id == projects[0].id
    assert len(result_project.tasks) == 3
    for task in result_project.tasks:
        assert task.project_id == projects[0].id
