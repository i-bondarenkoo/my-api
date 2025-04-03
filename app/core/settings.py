from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5439/postgres"
    db_echo: bool = True


settings = Settings()
