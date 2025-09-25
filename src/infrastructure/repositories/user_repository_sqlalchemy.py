from collections.abc import AsyncGenerator
from typing import List
from uuid import UUID

from sqlalchemy import delete, select, update
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
        query = await self.session.execute(query)
        result = query.scalar_one_or_none()

        if result:
            return User(
                id=str(result.id),
                name=result.name,
                email=result.email,
                password=result.password,
                role=result.role,
                avatar=result.avatar,
                created_at=result.created_at,
            )

    async def find_by_id(self, user_id: str) -> User | None:
        """
        Find a user baed on its id.

        :param user_id: Serch id.

        :return: The user if found and None otherwise.
        """
        query = select(UserModel).filter(UserModel.id == UUID(user_id))
        query = await self.session.execute(query)
        result = query.scalar_one_or_none()

        if result:
            return User(
                id=str(result.id),
                name=result.name,
                email=result.email,
                password=result.password,
                role=result.role,
                avatar=result.avatar,
                created_at=result.created_at,
            )

    async def find_all(self) -> List[User]:
        """
        Find all users.

        :param user_id: Serch id.

        :return: The user if found and None otherwise.
        """
        query = select(UserModel)
        query = await self.session.execute(query)
        result = query.scalars()

        users: List[User] = []

        for r in result:
            users.append(
                User(
                    id=str(r.id),
                    name=r.name,
                    email=r.email,
                    password=r.password,
                    role=r.role,
                    avatar=r.avatar,
                    created_at=r.created_at,
                )
            )

        return users

    async def delete_by_id(self, user_id: str) -> None:
        """
        Delete a user baed on its id.

        :param user_id: Serch id.

        :return: None.
        """
        query = delete(UserModel).filter(UserModel.id == user_id)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, user: User) -> User:
        """
        Update a user baed on its id.

        :param user: User entity to update.

        :return: The updated User entity.
        """
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                name=user.name,
                password=user.password,
                role=user.role,
                avatar=user.avatar,
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

        return user
