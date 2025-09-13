from pydantic import BaseModel, EmailStr

from src.domain.entities.user_role import UserRole


class AuthLoginInputDTO(BaseModel):
    email: EmailStr
    password: str


class AuthLoginOutputDTO(BaseModel):
    id: str
    name: str
    role: UserRole
    avatar: str
