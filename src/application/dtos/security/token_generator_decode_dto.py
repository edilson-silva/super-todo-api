from pydantic import BaseModel

from src.domain.entities.user_role import UserRole


class TokenGeneratorDecodeOutputDTO(BaseModel):
    user_id: str
    user_role: UserRole
    company_id: str
