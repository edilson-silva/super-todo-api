from collections.abc import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_entity import User
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException
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
        try:
            user_model = UserModel(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                role=user.role,
                avatar=user.avatar,
                created_at=user.created_at,
            )
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)

            return user
        except IntegrityError:
            raise UserAlreadyExistsException()

    async def find_by_email(self, email: str) -> User | None:
        """
        Find a user baed on its email.

        :param email: Serch email.

        :return: The user if found and None otherwise.
        """
        query = select(UserModel).filter(UserModel.email == email)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()
