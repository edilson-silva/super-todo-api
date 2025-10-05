from abc import ABC, abstractmethod

from src.application.dtos.security.token_generator_decode_dto import (
    TokenGeneratorDecodeOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
    TokenGeneratorEncodeOutputDTO,
)


class TokenGenerator(ABC):
    @abstractmethod
    async def async_encode(
        self, payload: TokenGeneratorEncodeInputDTO
    ) -> TokenGeneratorEncodeOutputDTO:
        """
        Generate a token based on payload.

        :param payload: The token payload.

        :return: The generated token.
        """
        pass

    @abstractmethod
    async def async_decode(
        self, access_token: str
    ) -> TokenGeneratorDecodeOutputDTO:
        """
        Decode an access_token.

        :param access_token: The access token to be decoded.

        :return: The token payload.
        """
        pass
