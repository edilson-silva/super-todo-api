from datetime import datetime, timedelta, timezone

from jwt import decode, encode

from src.application.dtos.security.token_generator_decode_dto import (
    TokenGeneratorDecodeOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
    TokenGeneratorEncodeOutputDTO,
)
from src.core.settings import settings
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import InvalidTokenException
from src.domain.security.token_generator import TokenGenerator


class TokenGeneratorPyJWT(TokenGenerator):
    def __init__(self):
        self.secret_key = settings.ACCESS_TOKEN_SECRET_KEY
        self.algorithm = settings.ACCESS_TOKEN_ALGORITHM
        self.expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.token_type = settings.ACCESS_TOKEN_TYPE

    async def async_encode(
        self, payload: TokenGeneratorEncodeInputDTO
    ) -> TokenGeneratorEncodeOutputDTO:
        """
        Generate a token based on payload.

        :param payload: The token payload.

        :return: The generated token.
        """
        exp = datetime.now(tz=timezone.utc) + timedelta(
            minutes=self.expire_minutes
        )

        token_payload = {
            'sub': payload.user_id,
            'role': payload.user_role,
            'company': payload.company_id,
            'exp': exp,
        }
        token = encode(
            token_payload,
            self.secret_key,
            algorithm=self.algorithm,
        )
        return TokenGeneratorEncodeOutputDTO(
            token=token, token_type=self.token_type
        )

    async def async_decode(
        self, access_token: str
    ) -> TokenGeneratorDecodeOutputDTO | None:
        """
        Decode an access_token.

        :param access_token: The access token to be decoded.

        :return: The token payload if valid or None otherwise.
        """
        try:
            decoded = decode(
                access_token, self.secret_key, algorithms=[self.algorithm]
            )

            return TokenGeneratorDecodeOutputDTO(
                user_id=decoded['sub'],
                user_role=UserRole(decoded['role']),
                company_id=decoded['company'],
            )
        except InvalidTokenException:
            return None
