import pytest
from app import crud
from sqlalchemy import select
from app.schemas.project import ResponseProject, CreateProject
from app.models.project import ProjectOrm


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
async def test_create_project(create_project, project_data, session_test_db):
    assert create_project is not None
    assert create_project.title == project_data.title
    assert create_project.description == project_data.description
    assert create_project.status == project_data.status
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
