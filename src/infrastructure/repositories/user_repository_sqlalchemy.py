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
                company_id=UUID(str(user.company_id)),
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)

            user.id = str(user.id)

            return user
        except IntegrityError:
            raise UserAlreadyExistsException()

    async def find_by_email(self, email: str) -> User | None:
        """
        Find a user baed on its email.

        :param email: Serch email.

        :return: The user if found and None otherwise.
        """
        stmt = select(UserModel).filter(UserModel.email == email)
        query = await self.session.execute(stmt)
        result = query.scalar_one_or_none()

        if result:
            return User(
                id=str(result.id),
                name=result.name,
                email=result.email,
                password=result.password,
                role=result.role,
                avatar=result.avatar,
                company_id=result.company_id,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )

    async def find_by_id(self, user_id: str, company_id: str) -> User | None:
        """
        Find a user baed on its id.

        :param user_id: Serch id.
        :param company_id: Id of the company the user belongs to.

        :return: The user if found and None otherwise.
        """
        stmt = select(UserModel).filter(
            UserModel.id == UUID(user_id),
            UserModel.company_id == UUID(company_id),
        )
        query = await self.session.execute(stmt)
        result = query.scalar_one_or_none()

        if result:
            return User(
                id=str(result.id),
                name=result.name,
                email=result.email,
                password=result.password,
                role=result.role,
                avatar=result.avatar,
                company_id=result.company_id,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )

    async def find_all(self, limit: int, offset: int) -> List[User]:
        """
        Find all users.

        :param limit: Maximum number of users returned.
        :param offset: Number of users ignored in the search.

        :return: The user if found and None otherwise.
        """
        stmt = select(UserModel).limit(limit).offset(offset)
        query = await self.session.execute(stmt)
        results = query.scalars()

        users: List[User] = []

        for result in results:
            users.append(
                User(
                    id=str(result.id),
                    name=result.name,
                    email=result.email,
                    password=result.password,
                    role=result.role,
                    avatar=result.avatar,
                    company_id=result.company_id,
                    created_at=result.created_at,
                    updated_at=result.updated_at,
                )
            )

        return users

    async def delete_by_id(self, user_id: str) -> None:
        """
        Delete a user baed on its id.

        :param user_id: Serch id.

        :return: None.
        """
        stmt = delete(UserModel).filter(UserModel.id == UUID(user_id))
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, user: User) -> User:
        """
        Update a user baed on its id.

        :param user: User entity to update.

        :return: The updated User entity.
        """
        stmt = (
            update(UserModel)
            .where(UserModel.id == UUID(str(user.id)))
            .values(
                name=user.name,
                password=user.password,
                role=user.role,
                avatar=user.avatar,
                updated_at=user.updated_at,
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

        user.id = str(user.id)

        return user
