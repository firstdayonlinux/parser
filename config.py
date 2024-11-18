from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator, RedisDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class InfrastructureConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int = 5432
    db_driver: str = "postgresql"

    app_redis_port: int
    app_redis_host: str
    app_redis_db: str

    postgres_dsn: PostgresDsn | None = None
    redis_dsn: RedisDsn | None = None

    @field_validator("postgres_dsn", mode="after")
    @classmethod
    def get_postgres_dsn(cls, _, info: ValidationInfo):
        return PostgresDsn.build(
            username=info.data["db_user"],
            password=info.data["db_password"],
            path=info.data["db_name"],
            host=info.data["db_host"],
            port=info.data["db_port"],
            scheme=info.data["db_driver"],
        )

    @field_validator('redis_dsn', mode='after')
    @classmethod
    def get_redis_dsn(cls, _, info: ValidationInfo):
        return RedisDsn.build(
            scheme='redis',
            host=info.data['app_redis_host'],
            port=info.data['app_redis_port'],
            path=info.data['app_redis_db'],
        )


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='api_')

    HOST: str = '0.0.0.0'
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 1
    ALLOWED_HOSTS: list[str] = ['*']


class Settings(BaseSettings):
    infrastructure_config: InfrastructureConfig = InfrastructureConfig()
    api_config: ApiConfig = ApiConfig()


settings = Settings()