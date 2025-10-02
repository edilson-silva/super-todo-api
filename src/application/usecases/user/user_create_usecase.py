from src.application.dtos.user.user_create_dto import (
    UserCreateInputDTO,
    UserCreateOutputDTO,
)
from src.domain.entities.user_entity import User
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class UserCreateUseCase:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ):
        """
        :param repository: UserRepository instance to interact with user.
        :param password_hasher: PasswordHasher instance to hash user password.
        """
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(self, data: UserCreateInputDTO) -> UserCreateOutputDTO:
        """
        Create a new user and store it in the repository.

        :param name: The name of the user.
        :param email: The email of the user.
        :param password: The password of the user.

        :return: The created User entity.
        """
        user = await self.repository.find_by_email(data.email)

        if user:
            raise UserAlreadyExistsException()

        hashed_password = await self.password_hasher.async_hash(data.password)

        user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            role=data.role,
            avatar=data.avatar,
            company_id=data.company_id,
        )

        created_user: User = await self.repository.create(user)
        return UserCreateOutputDTO.model_validate(created_user)
