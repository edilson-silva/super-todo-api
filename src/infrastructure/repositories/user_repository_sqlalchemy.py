from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_entity import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.db.models.user_model import UserModel


class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
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
