import pytest

from src.application.dtos.auth.auth_signin_dto import (
    AuthSigninInputDTO,
    AuthSigninOutputDTO,
)
from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.core.settings import settings
from src.domain.entities.user_entity import User
from src.domain.exceptions.auth_exceptions import InvalidCredentialsException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.company_repository import CompanyRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator


@pytest.mark.asyncio
class TestAuthSigninUsecase:
    async def test_valid_credentials_should_return_access_token(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
        admin_user: User,
        admin_user_info: dict,
    ):
        signin_dto = AuthSigninInputDTO(
            email=admin_user_info['email'],
            password=admin_user_info['password'],
        )
        signin_usecase = AuthSigninUseCase(
            user_repository, password_hasher, token_generator
        )

        response = await signin_usecase.execute(signin_dto)

        assert isinstance(response, AuthSigninOutputDTO)
        assert isinstance(response.access_token, str)
        assert response.access_token != ''
        assert isinstance(response.token_type, str)
        assert response.token_type == settings.ACCESS_TOKEN_TYPE

    async def test_invalid_credentials_should_raise_exception(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
        admin_user: User,
        admin_user_info: dict,
    ):
        signin_dto = AuthSigninInputDTO(
            email=admin_user_info['email'],
            password='{}_err'.format(admin_user_info['password']),
        )
        signin_usecase = AuthSigninUseCase(
            user_repository, password_hasher, token_generator
        )

        with pytest.raises(InvalidCredentialsException) as exc:
            await signin_usecase.execute(signin_dto)

        assert str(exc.value) == 'Invalid credentials'

    async def test_not_found_user_should_raise_exception(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
        admin_user_info: dict,
    ):
        signin_dto = AuthSigninInputDTO(
            email=admin_user_info['email'],
            password='{}_err'.format(admin_user_info['password']),
        )

        signin_usecase = AuthSigninUseCase(
            user_repository, password_hasher, token_generator
        )

        with pytest.raises(NotFoundException) as exc:
            await signin_usecase.execute(signin_dto)

        assert str(exc.value) == 'Not found'
