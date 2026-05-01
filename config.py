from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        env_prefix="",
    )

    # App
    APP_NAME: str = "training-app"
    ENVIRONMENT: str = "development"

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = Field(alias="PGPORT")
    DATABASE_URL: str

    #redis
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int

    #elasicsearch
    ELASTICSEARCH_USER: str
    ELASTICSEARCH_PASSWORD: str
    ELASTICSEARCH_URL: str

    # Security
    PRIVATE_KEY: str
    PUBLIC_KEY: str = Field(alias="PUBLIC_KEY")

    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()