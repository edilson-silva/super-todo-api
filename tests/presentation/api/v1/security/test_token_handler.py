import pytest

from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeOutputDTO,
)
from src.domain.entities.user_entity import User
from src.domain.exceptions.auth_exceptions import (
    InvalidTokenException,
    UnauthorizedException,
)
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.token_generator import TokenGenerator
from src.presentation.api.v1.security.token_handler import (
    get_requester_from_token,
)


@pytest.mark.asyncio
class TestGetRequesterFromToken:
    async def test_empty_token_should_raise_invalid_token_exception(
        self,
        empty_token: TokenGeneratorEncodeOutputDTO,
        token_generator: TokenGenerator,
        user_repository: UserRepository,
    ):
        with pytest.raises(InvalidTokenException) as exc_info:
            await get_requester_from_token(
                empty_token.access_token, token_generator, user_repository
            )

        assert str(exc_info.value) == 'Invalid token'

    async def test_invalid_token_body_should_raise_invalid_token_exception(
        self,
        token_generator: TokenGenerator,
        user_repository: UserRepository,
    ):
        with pytest.raises(InvalidTokenException) as exc_info:
            await get_requester_from_token(
                'invalid-token', token_generator, user_repository
            )

        assert str(exc_info.value) == 'Invalid token'

    async def test_invalid_token_should_raise_invalid_token_exception(
        self,
        invalid_token: TokenGeneratorEncodeOutputDTO,
        token_generator: TokenGenerator,
        user_repository: UserRepository,
    ):
        with pytest.raises(InvalidTokenException) as exc_info:
            await get_requester_from_token(
                invalid_token.access_token, token_generator, user_repository
            )

        assert str(exc_info.value) == 'Invalid token'

    async def test_invalid_user_token_should_raise_invalid_token_exception(
        self,
        invalid_user_token: TokenGeneratorEncodeOutputDTO,
        token_generator: TokenGenerator,
        user_repository: UserRepository,
    ):
        with pytest.raises(UnauthorizedException) as exc_info:
            await get_requester_from_token(
                invalid_user_token.access_token,
                token_generator,
                user_repository,
            )

        assert str(exc_info.value) == 'Unauthorized'

    async def test_valid_token_should_return_user(
        self,
        admin_user: User,
        admin_user_token: TokenGeneratorEncodeOutputDTO,
        token_generator: TokenGenerator,
        user_repository: UserRepository,
    ):
        user = await get_requester_from_token(
            admin_user_token.access_token,
            token_generator,
            user_repository,
        )

        assert isinstance(user, User)
        assert user.id == admin_user.id
        assert user.email == admin_user.email
        assert user.role == admin_user.role
        assert user.password == admin_user.password
        assert user.avatar == admin_user.avatar
        assert user.company_id == admin_user.company_id
        assert user.created_at == admin_user.created_at
        assert user.updated_at == admin_user.updated_at
