from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import CreateTask, PartialUpdateTask
from app.models.task import TaskOrm
from sqlalchemy import select


async def create_task_crud(task: CreateTask, session: AsyncSession):
    new_task = TaskOrm(**task.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def get_task_by_id_crud(task_id: int, session: AsyncSession):
    current_task = await session.get(TaskOrm, task_id)
    return current_task


async def get_list_task_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(TaskOrm).order_by(TaskOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_task_partial_crud(
    task: PartialUpdateTask, task_id: int, session: AsyncSession
):
    update_task = await session.get(TaskOrm, task_id)
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(update_task, key, value)
    await session.commit()
    await session.refresh(update_task)
    return update_task


async def delete_task_crud(task_id: int, session: AsyncSession):
    current_task = await session.get(TaskOrm, task_id)
    await session.delete(current_task)
    await session.commit()
    return {
        "message": "Задача успешно удалена",
    }
