from pydantic import BaseModel, EmailStr


class AuthSignupInputDTO(BaseModel):
    company_name: str
    name: str
    email: EmailStr
    password: str
