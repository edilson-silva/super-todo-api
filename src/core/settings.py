from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    DEBUG: bool = Field(default=False, env='DEBUG')
    APP_NAME: str = Field(default='SuperTodo', env='APP_NAME')

    class Config:
        env_file = '.env'
        case_sensitive = True

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(('sqlite', 'postgresql', 'postgresql+asyncpg')):
            raise ValueError(
                'DATABASE_URL must be a valid SQLite or PostgreSQL URL'
            )
        return v


settings = Settings()
