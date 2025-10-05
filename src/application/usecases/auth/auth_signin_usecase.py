from src.application.dtos.auth.auth_signin_dto import (
    AuthSigninInputDTO,
    AuthSigninOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
)
from src.domain.exceptions.auth_exceptions import InvalidCredentialsException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator


class AuthSigninUseCase:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ):
        """
        :param repository: UserRepository instance to interact with user.
        :param password_hasher: PasswordHasher instance to hash user password.
        :param token_genrator: TokenGenerator instance to generate a token.
        """
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    async def execute(self, data: AuthSigninInputDTO) -> AuthSigninOutputDTO:
        """
        Perform signin getting user info.

        :param data: The user signin data.

        :return: Found user info.
        """
        user = await self.repository.find_by_email(data.email)

        if not user:
            raise NotFoundException()

        valid_password = await self.password_hasher.async_check(
            data.password, user.password
        )

        if not valid_password:
            raise InvalidCredentialsException()

        token_payload = TokenGeneratorEncodeInputDTO(
            user_id=str(user.id),
            user_role=user.role,
            company_id=str(user.company_id),
        )
        generated_token = await self.token_generator.async_encode(
            token_payload
        )

        return AuthSigninOutputDTO(
            token=generated_token.token, token_type=generated_token.token_type
        )
