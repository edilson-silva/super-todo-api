from dataclasses import replace
from datetime import datetime, timezone

from src.application.dtos.user.user_update_partial_dto import (
    UserUpdatePartialInputDTO,
    UserUpdatePartialOutputDTO,
)
from src.domain.entities.user_entity import User
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class UserUpdatePartialUseCase:
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
        self, user_id: str, company_id: str, data: UserUpdatePartialInputDTO
    ) -> UserUpdatePartialOutputDTO:
        """
        Update an user info based on its id.

        :param user_id: Id of user to update.
        :param company_id: Id of the company the user belongs to.
        :param data: User new data.

        :return: The updated User entity.
        """
        user = await self.repository.find_by_id(user_id, company_id)

        if not user:
            raise NotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return UserUpdatePartialOutputDTO.model_validate(user)

        user = replace(user, **update_data)
        user.updated_at = datetime.now(timezone.utc)

        updated_user: User = await self.repository.update(user)
        return UserUpdatePartialOutputDTO.model_validate(updated_user)
