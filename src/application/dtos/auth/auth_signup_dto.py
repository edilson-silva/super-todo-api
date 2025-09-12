from pydantic import BaseModel, EmailStr


class AuthSignupInputDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
