from pydantic import BaseModel


class TokenDTO(BaseModel):
    token: str
    token_type: str = 'Bearer'
