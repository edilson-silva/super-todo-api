import pytest

from src.application.dtos.auth.auth_signin_dto import (
    AuthSigninInputDTO,
    AuthSigninOutputDTO,
)
from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.core.settings import settings
from src.domain.exceptions.auth_exceptions import InvalidCredentialsException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator


@pytest.mark.asyncio
class TestAuthSigninUsecase:
    async def test_login_with_valid_credentials_should_return_access_token(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
        fake_token_generator: TokenGenerator,
    ):
        name = 'test'
        email = 'test@example.com'
        password = '123456789'

        signup_dto = AuthSignupInputDTO(
            name=name,
            email=email,
            password=password,
        )
        signup_usecase = AuthSignupUseCase(
            fake_user_repository, fake_password_hasher
        )
        await signup_usecase.execute(data=signup_dto)

        signin_dto = AuthSigninInputDTO(
            email=email,
            password=password,
        )
        signin_usecase = AuthSigninUseCase(
            fake_user_repository, fake_password_hasher, fake_token_generator
        )

        response = await signin_usecase.execute(signin_dto)

        assert isinstance(response, AuthSigninOutputDTO)
        assert (
            response.access_token == f'{settings.ACCESS_TOKEN_TYPE} fake_token'
        )

    async def test_login_with_invalid_credentials_should_raise_exception(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
        fake_token_generator: TokenGenerator,
    ):
        name = 'test'
        email = 'test@example.com'
        signup_password = '123456789'
        signin_password = '1234567890'

        signup_dto = AuthSignupInputDTO(
            name=name,
            email=email,
            password=signup_password,
        )
        signup_usecase = AuthSignupUseCase(
            fake_user_repository, fake_password_hasher
        )
        await signup_usecase.execute(data=signup_dto)

        signin_dto = AuthSigninInputDTO(
            email=email,
            password=signin_password,
        )
        signin_usecase = AuthSigninUseCase(
            fake_user_repository, fake_password_hasher, fake_token_generator
        )

        with pytest.raises(InvalidCredentialsException) as exc:
            await signin_usecase.execute(signin_dto)

        assert str(exc.value) == 'Invalid credentials'

    async def test_login_with_non_existing_user_should_raise_exception(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
        fake_token_generator: TokenGenerator,
    ):
        email = 'test@example.com'
        password = '123456789'

        signup_dto = AuthSigninInputDTO(
            email=email,
            password=password,
        )
        signin_usecase = AuthSigninUseCase(
            fake_user_repository, fake_password_hasher, fake_token_generator
        )

        with pytest.raises(NotFoundException) as exc:
            await signin_usecase.execute(signup_dto)

        assert str(exc.value) == 'Not found'
