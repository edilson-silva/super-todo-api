from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateInputDTO(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreateOutputDTO(BaseModel):
    id: str
    name: str
    email: str
    password: str
    created_at: datetime

    class Config:
        from_attributes = True  # allow conversion from dataclass/ORM
