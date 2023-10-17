from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gateway_db_url: str = "sqlite:///sql_app.db"


settings = Settings()
