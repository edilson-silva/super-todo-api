from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', case_sensitive=True
    )

    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    DEBUG: bool = Field(default=False, env='DEBUG')
    APP_NAME: str = Field(default='SuperTodo', env='APP_NAME')
    ACCESS_TOKEN_TYPE: str = Field(default='Bearer', env='ACCESS_TOKEN_TYPE')
    ACCESS_TOKEN_ALGORITHM: str = Field(
        default='HS256', env='ACCESS_TOKEN_ALGORITHM'
    )
    ACCESS_TOKEN_SECRET_KEY: str = Field(..., env='ACCESS_TOKEN_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, env='ACCESS_TOKEN_EXPIRE_MINUTES'
    )

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(('sqlite', 'postgresql', 'postgresql+asyncpg')):
            raise ValueError(
                'DATABASE_URL must be a valid SQLite or PostgreSQL URL'
            )
        return v


settings = Settings()
