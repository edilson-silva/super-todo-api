from fastapi import APIRouter

from src.presentation.api.v1 import user_controller

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(user_controller.router)
