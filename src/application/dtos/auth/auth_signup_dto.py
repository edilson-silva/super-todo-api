from pydantic import BaseModel, EmailStr


class AuthSignupInputDTO(BaseModel):
    company_name: str
    user_name: str
    user_email: EmailStr
    user_password: str
