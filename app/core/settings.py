from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # основная база данных
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5439/postgres"
    # тестовая база данных
    test_db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5440/test_db"
    db_echo: bool = True

    secret_key: str = "e7e2385e08e4d3d2905ddca286ecdabfb6a00169a44ff328f4a5e878b8e1e9c7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


settings = Settings()
