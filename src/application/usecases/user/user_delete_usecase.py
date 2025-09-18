from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository


class UserDeleteUseCase:
    def __init__(self, repository: UserRepository):
        """
        :param repository: UserRepository instance to interact with user.
        """
        self.repository = repository

    async def execute(self, user_id: str) -> None:
        """
        Delete a user based on its id.

        :param user_id: Id used to get user.

        :return: None.
        """
        user = await self.repository.find_by_id(user_id)

        if not user:
            raise NotFoundException()

        await self.repository.delete_by_id(user_id)
