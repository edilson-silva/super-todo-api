from pydantic import BaseModel, EmailStr


class AuthSigninInputDTO(BaseModel):
    email: EmailStr
    password: str


class AuthSigninOutputDTO(BaseModel):
    access_token: str
