from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from starlette.responses import RedirectResponse

from src.presentation.api.v1.security.exceptions_handler import (
    http_exception_handler,
)

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


app = FastAPI(
    title=settings.APP_NAME,
    version='1.0.0',
    lifespan=lifespan,
    root_path='/api/v1',
)
http_exception_handler(app)


@app.get('/')
async def read_root():
    return RedirectResponse(
        url='/docs', status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


app.include_router(api_router)
