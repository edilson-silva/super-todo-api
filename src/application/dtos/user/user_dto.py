from datetime import datetime

from src.domain.entities.user_role import UserRole

from ..base_dto import BaseDTO


class UserOutputDTO(BaseDTO):
    id: str
    name: str
    email: str
    role: UserRole
    avatar: str
    created_at: datetime
