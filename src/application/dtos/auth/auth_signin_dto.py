from pydantic import BaseModel, EmailStr

from src.application.dtos.auth.token_dto import TokenDTO


class AuthSigninInputDTO(BaseModel):
    email: EmailStr
    password: str


class AuthSigninOutputDTO(TokenDTO):
    pass
