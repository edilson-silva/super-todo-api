from typing import Optional

from src.domain.entities.user_role import UserRole

from ..base_dto import BaseDTO
from .user_output_dto import UserOutputDTO


class UserUpdateInputDTO(BaseDTO):
    name: str
    password: str
    role: Optional[UserRole] = UserRole.ADMIN
    avatar: Optional[str] = ''


class UserUpdateOutputDTO(UserOutputDTO):
    pass
