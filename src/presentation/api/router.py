from fastapi import APIRouter

from src.presentation.api.v1.routes import auth_controller, user_controller

api_router = APIRouter()
api_router.include_router(auth_controller.router)
api_router.include_router(user_controller.router)
