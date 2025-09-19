from src.domain.entities.user_role import UserRole

from ..base_dto import BaseDTO
from .user_output_dto import UserOutputDTO


class UserUpdateInputDTO(BaseDTO):
    name: str
    password: str
    role: UserRole
    avatar: str


class UserUpdateOutputDTO(UserOutputDTO):
    pass
