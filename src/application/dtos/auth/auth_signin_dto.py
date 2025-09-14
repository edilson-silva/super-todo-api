from pydantic import BaseModel, EmailStr

from src.domain.entities.user_role import UserRole


class AuthSigninInputDTO(BaseModel):
    email: EmailStr
    password: str


class AuthSigninOutputDTO(BaseModel):
    id: str
    name: str
    role: UserRole
    avatar: str
