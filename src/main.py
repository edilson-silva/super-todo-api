from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.settings import settings
from .infrastructure.db.session import Base, engine
from .presentation.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # Shutdown (engine cleanup)
    await engine.dispose()


app = FastAPI(title=settings.APP_NAME, version='1.0.0', lifespan=lifespan)

app.include_router(api_router)
