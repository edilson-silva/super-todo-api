from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.dtos.user.user_output_dto import UserOutputDTO
from src.domain.repositories.user_repository import UserRepository


class UserListUseCase:
    def __init__(self, repository: UserRepository):
        """
        :param repository: UserRepository instance to interact with user.
        """
        self.repository = repository

    async def execute(self, limit: int, offset: int) -> UserListOutputDTO:
        """
        Get the list of users.

        :param limit: Maximum number of users returned.
        :param offset: Number of users ignored in the search.

        :return: List of users.
        """
        users = await self.repository.find_all(limit, offset)

        users_output_dto = UserListOutputDTO(
            data=list(map(lambda u: UserOutputDTO.model_validate(u), users))
        )

        return users_output_dto
