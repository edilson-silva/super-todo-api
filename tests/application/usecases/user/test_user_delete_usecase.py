import pytest

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
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
    ):
        user_create_dto = UserCreateInputDTO(
            name='Test User',
            email='test@example.com',
            password='123456789',
        )
        user_create_usecase = UserCreateUseCase(
            fake_user_repository, fake_password_hasher
        )

        user_created = await user_create_usecase.execute(user_create_dto)

        user_delete_usecase = UserDeleteUseCase(fake_user_repository)

        user_deleted = await user_delete_usecase.execute(user_created.id)

        assert user_deleted is None

    async def test_invalid_id_should_raise_exception(
        self,
        fake_user_repository: UserRepository,
    ):
        user_delete_usecase = UserDeleteUseCase(fake_user_repository)

        with pytest.raises(NotFoundException) as exc:
            await user_delete_usecase.execute('random-uuid')

        assert str(exc.value) == 'Not found'
