from fastapi import FastAPI, status
from starlette.responses import RedirectResponse

from src.core.settings import settings
from src.presentation.api.router import api_router
from src.presentation.api.v1.security.exceptions_handler import (
    http_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    version='1.0.0',
    root_path='/api/v1',
)
http_exception_handler(app)


@app.get('/')
async def read_root():
    return RedirectResponse(
        url='/docs', status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )


app.include_router(api_router)
