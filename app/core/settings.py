from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # основная база данных
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5439/postgres"
    # тестовая база данных
    test_db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5440/test_db"
    db_echo: bool = True


settings = Settings()
