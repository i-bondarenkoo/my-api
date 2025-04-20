from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.settings import settings

test_engine = create_async_engine(
    url=settings.test_db_url,
    echo=settings.db_echo,
)

# фабрика сессий
TestSession = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def get_testdb_session():
    async with TestSession() as test_session:
        yield test_session
