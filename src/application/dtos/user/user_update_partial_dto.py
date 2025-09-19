from typing import Optional

from src.domain.entities.user_role import UserRole

from ..base_dto import BaseDTO
from .user_output_dto import UserOutputDTO


class UserUpdatePartialInputDTO(BaseDTO):
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    avatar: Optional[str] = None


class UserUpdatePartialOutputDTO(UserOutputDTO):
    pass
