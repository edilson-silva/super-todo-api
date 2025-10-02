from jwt import decode, encode

from src.application.dtos.security.token_generator_decode_dto import (
    TokenGeneratorDecodeOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
)
from src.core.settings import settings
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import InvalidTokenException
from src.domain.security.token_generator import TokenGenerator


class TokenGeneratorPyJWT(TokenGenerator):
    def __init__(self):
        self.secret_key = settings.ACCESS_TOKEN_SECRET_KEY
        self.algorithm = settings.ACCESS_TOKEN_ALGORITHM

    async def async_encode(self, payload: TokenGeneratorEncodeInputDTO) -> str:
        """
        Generate a token based on payload.

        :param payload: The token payload.

        :return: The generated token.
        """
        token_payload = {
            'sub': payload.user_id,
            'role': payload.user_role,
            'company': payload.company_id,
        }
        token = encode(
            token_payload, self.secret_key, algorithm=self.algorithm
        )
        return f'{settings.ACCESS_TOKEN_TYPE} {token}'

    async def async_decode(
        self, access_token: str
    ) -> TokenGeneratorDecodeOutputDTO:
        """
        Decode an access_token.

        :param access_token: The access token to be decoded.

        :return: The token payload.
        """
        try:
            decoded = decode(
                access_token, self.secret_key, algorithms=[self.algorithm]
            )

            return TokenGeneratorDecodeOutputDTO(
                user_id=decoded['token_id'],
                user_role=UserRole[decoded['token_role']],
            )
        except InvalidTokenException:
            raise InvalidTokenException()
