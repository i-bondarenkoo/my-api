from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import USER_NOT_FOUND_EXCEPTION, NO_DATA_FOR_UPDATES
from app.schemas.user import CreateUser, PatchUpdateUser
from app.models.user import UserOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_user_crud(user_in: CreateUser, session: AsyncSession):
    new_user = UserOrm(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id(user_id: int, session: AsyncSession):
    user = await session.get(UserOrm, user_id)
    return user


async def get_list_users_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(UserOrm).order_by(UserOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_user_patch_crud(
    user: PatchUpdateUser, user_id: int, session: AsyncSession
):
    update_user = await session.get(UserOrm, user_id)
    if not update_user:
        raise USER_NOT_FOUND_EXCEPTION
    data = user.model_dump(exclude_unset=True)
    # проверка что пользователь передал какие-то данные для обновления
    if not data:
        raise NO_DATA_FOR_UPDATES
    for key, value in data.items():
        setattr(update_user, key, value)
    await session.commit()
    await session.refresh(update_user)
    return update_user


async def delete_user_crud(user_id: int, session: AsyncSession):
    current_user = await session.get(UserOrm, user_id)
    if not current_user:
        raise USER_NOT_FOUND_EXCEPTION
    await session.delete(current_user)
    await session.commit()
    return {
        "message": "Пользователь успешно удален",
    }


# получить пользователя с проектами и задачами
async def get_user_with_details_crud(user_id: int, session: AsyncSession):
    user = await get_user_by_id(user_id, session)
    if not user:
        raise USER_NOT_FOUND_EXCEPTION
    # подгружаем связи
    stmt = (
        select(UserOrm)
        .where(UserOrm.id == user_id)
        .options(
            selectinload(UserOrm.tasks),
            selectinload(UserOrm.projects),
        )
    )
    result = await session.execute(stmt)
    return result.scalars().first()
