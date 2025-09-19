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
        self, user_id: str, data: UserUpdatePartialInputDTO
    ) -> UserUpdatePartialOutputDTO:
        """
        Update an user info based on its id.

        :param id: Id of user to update
        :param data: User new data.

        :return: The updated User entity.
        """
        user = await self.repository.find_by_id(user_id)

        if not user:
            raise NotFoundException()

        if data.name:
            user.name = data.name

        if data.password:
            hashed_password = await self.password_hasher.async_hash(
                data.password
            )
            user.password = hashed_password

        if data.role:
            user.role = data.role

        if data.avatar:
            user.avatar = data.avatar

        updated_user: User = await self.repository.update(user)
        return UserUpdatePartialOutputDTO.model_validate(updated_user)
