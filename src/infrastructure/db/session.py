from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.settings import settings

# Async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base model
Base = declarative_base()


# Dependency to yield a session per request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a fresh database session for the current request.

    :return: An instance of AsyncSession.
    """
    async with AsyncSessionLocal() as session:
        yield session
