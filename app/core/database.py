from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.settings import settings

# движок
engine = create_async_engine(
    url=settings.db_url,
    echo=settings.db_echo,
)

# фабрика  сессии
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


# зависимость для получения сессии
async def get_db_session():
    async with AsyncSession() as session:
        yield session
