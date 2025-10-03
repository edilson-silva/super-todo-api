import pytest
from uuid_extensions import uuid7str

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_delete_usecase import UserDeleteUseCase
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserDeleteUsecase:
    async def test_valid_id_should_delete_and_return_success(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        company_id = uuid7str()

        user_create_dto = UserCreateInputDTO(
            name='Test User',
            email='test@example.com',
            password='123456789',
            company_id=company_id,
        )
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        user_created = await user_create_usecase.execute(user_create_dto)

        user_delete_usecase = UserDeleteUseCase(user_repository)

        user_deleted = await user_delete_usecase.execute(
            user_created.id, company_id
        )

        assert user_deleted is None

    async def test_invalid_id_should_raise_exception(
        self,
        user_repository: UserRepository,
    ):
        user_delete_usecase = UserDeleteUseCase(user_repository)

        with pytest.raises(NotFoundException) as exc:
            await user_delete_usecase.execute(uuid7str(), uuid7str())

        assert str(exc.value) == 'Not found'
