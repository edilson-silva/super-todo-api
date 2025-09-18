from src.application.dtos.user.user_get_dto import UserGetOutputDTO
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class UserGetUseCase:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ):
        """
        :param repository: UserRepository instance to interact with user.
        :param password_hasher: PasswordHasher instance to hash user password.
        """
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(self, user_id: str) -> UserGetOutputDTO:
        """
        Get a user based on its id.

        :param user_id: Id used to get user.

        :return: Found user info.
        """
        user = await self.repository.find_by_id(user_id)

        if not user:
            raise NotFoundException()

        return UserGetOutputDTO.model_validate(user)
