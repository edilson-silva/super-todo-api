from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository


class UserDeleteUseCase:
    def __init__(self, repository: UserRepository):
        """
        :param repository: UserRepository instance to interact with user.
        """
        self.repository = repository

    async def execute(self, requester: User, user_id: str) -> None:
        """
        Delete a user based on its id.

        :param requester: User trying to perform the action (must be an admin).
        :param user_id: Id of used to be deleted.

        :return: None.
        """
        if requester.role != UserRole.ADMIN:
            raise UnauthorizedException()

        user = await self.repository.find_by_id(user_id, requester.company_id)

        if not user:
            raise NotFoundException()

        if str(user.id) == str(requester.id):
            raise UnauthorizedException(
                'You are not allowed to delete your own account.'
            )

        await self.repository.delete_by_id(user_id, requester.company_id)
