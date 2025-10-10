from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.dtos.user.user_output_dto import UserOutputDTO
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.repositories.user_repository import UserRepository


class UserListUseCase:
    def __init__(self, repository: UserRepository):
        """
        :param repository: UserRepository instance to interact with user.
        """
        self.repository = repository

    async def execute(
        self, requester: User, limit: int, offset: int
    ) -> UserListOutputDTO:
        """
        Get the list of users.

        :param requester: User trying to perform the action (must be an admin).
        :param limit: Maximum number of users returned.
        :param offset: Number of users ignored in the search.

        :return: List of users.
        """
        if requester.role != UserRole.ADMIN:
            raise UnauthorizedException()

        users = await self.repository.find_all(
            requester.company_id, limit, offset
        )

        users_output_dto = UserListOutputDTO(
            data=list(map(lambda u: UserOutputDTO.model_validate(u), users))
        )

        return users_output_dto
