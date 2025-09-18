import pytest

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserGetUsecase:
    async def test_valid_id_should_return_found_user(
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

        user_get_usecase = UserGetUseCase(fake_user_repository)

        user_found = await user_get_usecase.execute(user_created.id)

        assert user_found.id == user_created.id
        assert user_found.name == user_created.name
        assert user_found.email == user_created.email
        assert user_found.role == user_created.role
        assert user_found.avatar == user_created.avatar
        assert user_found.created_at == user_created.created_at

    async def test_invalid_id_should_raise_exception(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
    ):
        user_get_usecase = UserGetUseCase(fake_user_repository)

        with pytest.raises(NotFoundException) as exc:
            await user_get_usecase.execute('random-uuid')

        assert str(exc.value) == 'Not found'
