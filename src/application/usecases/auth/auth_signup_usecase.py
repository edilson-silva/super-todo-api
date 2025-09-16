from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class AuthSignupUseCase:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ):
        """
        :param repository: UserRepository instance to interact with user.
        :param password_hasher: PasswordHasher instance to hash user password.
        """
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(self, data: AuthSignupInputDTO):
        """
        Perform signup creating an admin user.

        :param data: The user signup data.

        :return: No response.
        """
        user = await self.repository.find_by_email(data.email)

        if user:
            raise UserAlreadyExistsException()

        hashed_password = await self.password_hasher.async_hash(data.password)
        user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            role=UserRole.ADMIN,
        )

        await self.repository.create(user)
