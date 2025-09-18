from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.dtos.user.user_output_dto import UserOutputDTO
from src.domain.repositories.user_repository import UserRepository


class UserListUseCase:
    def __init__(self, repository: UserRepository):
        """
        :param repository: UserRepository instance to interact with user.
        """
        self.repository = repository

    async def execute(self) -> UserListOutputDTO:
        """
        Get the list of users.

        :return: List of users.
        """
        users = await self.repository.find_all()

        users_output_dto = UserListOutputDTO(
            data=list(map(lambda u: UserOutputDTO.model_validate(u), users))
        )

        return users_output_dto
