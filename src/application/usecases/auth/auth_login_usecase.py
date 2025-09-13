from src.application.dtos.auth.auth_login_dto import (
    AuthLoginInputDTO,
    AuthLoginOutputDTO,
)
from src.domain.exceptions.auth_exceptions import InvalidCredentialsException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class AuthLoginUseCase:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ):
        """
        :param repository: UserRepository instance to interact with user.
        :param password_hasher: PasswordHasher instance to hash user password.
        """
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(self, data: AuthLoginInputDTO) -> AuthLoginOutputDTO:
        """
        Perform login getting user info.

        :param data: The user login data.

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

        user_info = AuthLoginOutputDTO(
            id=str(user.id), name=user.name, role=user.role, avatar=user.avatar
        )

        return user_info
