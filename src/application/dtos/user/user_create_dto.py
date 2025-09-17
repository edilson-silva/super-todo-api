from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from src.domain.entities.user_role import UserRole

from ..base_dto import BaseDTO


class UserCreateInputDTO(BaseDTO):
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.ADMIN
    avatar: Optional[str] = ''


class UserCreateOutputDTO(BaseDTO):
    id: str
    name: str
    email: str
    role: UserRole
    avatar: str
    created_at: datetime
