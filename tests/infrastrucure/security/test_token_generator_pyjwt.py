from uuid_extensions import uuid7str

from src.application.dtos.security.token_generator_decode_dto import (
    TokenGeneratorDecodeOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
    TokenGeneratorEncodeOutputDTO,
)
from src.core.settings import settings
from src.domain.entities.user_role import UserRole
from src.domain.security.token_generator import TokenGenerator


class TestTokenGeneratorPyJWT:
    async def test_should_generate_a_token_with_exp_info(
        self, token_generator: TokenGenerator
    ):
        token_data = {
            'user_id': uuid7str(),
            'user_role': UserRole.ADMIN,
            'company_id': uuid7str(),
        }
        token_generator_input_dto = TokenGeneratorEncodeInputDTO(
            user_id=token_data['user_id'],
            user_role=token_data['user_role'],
            company_id=token_data['company_id'],
        )

        encoded_token = await token_generator.async_encode(
            token_generator_input_dto
        )

        assert isinstance(encoded_token, TokenGeneratorEncodeOutputDTO)
        assert encoded_token.access_token != ''
        assert encoded_token.token_type == settings.ACCESS_TOKEN_TYPE

        decoded_token = await token_generator.async_decode(
            encoded_token.access_token
        )

        assert isinstance(decoded_token, TokenGeneratorDecodeOutputDTO)
        assert decoded_token.user_id == token_data['user_id']
        assert decoded_token.user_role == token_data['user_role']
        assert decoded_token.company_id == token_data['company_id']
