from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_entity import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.db.models.user_model import UserModel


class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, session: AsyncGenerator[AsyncSession, None]):
        self.session = session

    async def create(self, user: User) -> User:
        """
        Create a new user in the database.

        :param user: User entity to create.

        :return: The created User entity.
        """
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            created_at=user.created_at,
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)

        return user
