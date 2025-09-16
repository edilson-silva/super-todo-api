from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.domain.entities.user_role import UserRole


class UserCreateInputDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.ADMIN
    avatar: Optional[str] = ''


class UserCreateOutputDTO(BaseModel):
    id: str
    name: str
    email: str
    password: str
    role: UserRole
    avatar: str
    created_at: datetime

    class Config:
        from_attributes = True  # allow conversion from dataclass/ORM
