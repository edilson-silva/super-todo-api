from fastapi import APIRouter

from src.presentation.api.v1 import auth_controller, user_controller

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(auth_controller.router)
api_router.include_router(user_controller.router)
