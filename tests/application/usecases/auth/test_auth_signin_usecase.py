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
    async def test_valid_credentials_should_return_access_token(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ):
        name = 'test'
        email = 'test@example.com'
        password = '123456789'

        signup_dto = AuthSignupInputDTO(
            name=name,
            email=email,
            password=password,
        )
        signup_usecase = AuthSignupUseCase(user_repository, password_hasher)
        await signup_usecase.execute(data=signup_dto)

        signin_dto = AuthSigninInputDTO(
            email=email,
            password=password,
        )
        signin_usecase = AuthSigninUseCase(
            user_repository, password_hasher, token_generator
        )

        response = await signin_usecase.execute(signin_dto)

        assert isinstance(response, AuthSigninOutputDTO)

        token_type, token_value = response.access_token.split()

        assert token_type == settings.ACCESS_TOKEN_TYPE
        assert token_type != ''

    async def test_invalid_credentials_should_raise_exception(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
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
        signup_usecase = AuthSignupUseCase(user_repository, password_hasher)
        await signup_usecase.execute(data=signup_dto)

        signin_dto = AuthSigninInputDTO(
            email=email,
            password=signin_password,
        )
        signin_usecase = AuthSigninUseCase(
            user_repository, password_hasher, token_generator
        )

        with pytest.raises(InvalidCredentialsException) as exc:
            await signin_usecase.execute(signin_dto)

        assert str(exc.value) == 'Invalid credentials'

    async def test_non_existing_user_should_raise_exception(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ):
        email = 'test@example.com'
        password = '123456789'

        signup_dto = AuthSigninInputDTO(
            email=email,
            password=password,
        )
        signin_usecase = AuthSigninUseCase(
            user_repository, password_hasher, token_generator
        )

        with pytest.raises(NotFoundException) as exc:
            await signin_usecase.execute(signup_dto)

        assert str(exc.value) == 'Not found'
