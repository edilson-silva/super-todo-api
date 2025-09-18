from typing import Optional

from pydantic import EmailStr

from src.domain.entities.user_role import UserRole

from ..base_dto import BaseDTO
from .user_dto import UserOutputDTO


class UserCreateInputDTO(BaseDTO):
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.ADMIN
    avatar: Optional[str] = ''


class UserCreateOutputDTO(UserOutputDTO):
    pass
