from datetime import datetime, timezone

from src.application.dtos.user.user_update_dto import (
    UserUpdateInputDTO,
    UserUpdateOutputDTO,
)
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class UserUpdateUseCase:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ):
        """
        :param repository: UserRepository instance to interact with user.
        :param password_hasher: PasswordHasher instance to hash user password.
        """
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(
        self, requester: User, user_id: str, data: UserUpdateInputDTO
    ) -> UserUpdateOutputDTO:
        """
        Update an user info based on its id.

        :param requester:
            User trying to perform the action
            (must be an admin or the own user).
        :param user_id: Id of user to update
        :param data: User new data.

        :return: The updated User entity.
        """
        user = await self.repository.find_by_id(user_id, requester.company_id)

        if not user:
            raise NotFoundException()

        if requester.role != UserRole.ADMIN and str(user.id) != str(
            requester.id
        ):
            raise UnauthorizedException(
                "You don't have enough permission to perform this action."
            )

        hashed_password = await self.password_hasher.async_hash(data.password)

        user.name = data.name
        user.password = hashed_password
        user.role = data.role
        user.avatar = data.avatar
        user.updated_at = datetime.now(timezone.utc)

        updated_user: User = await self.repository.update(user)
        return UserUpdateOutputDTO.model_validate(updated_user)
