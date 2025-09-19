import pytest

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.dtos.user.user_update_dto import (
    UserUpdateInputDTO,
    UserUpdateOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_update_usecase import UserUpdateUseCase
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserUpdateUsecase:
    async def test_valid_id_should_return_updated_user_info(
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

        user_update_dto = UserUpdateInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )
        user_update_usecase = UserUpdateUseCase(
            fake_user_repository, fake_password_hasher
        )

        user_updated = await user_update_usecase.execute(
            user_created.id, user_update_dto
        )

        assert isinstance(user_updated, UserUpdateOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_update_dto.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_update_dto.avatar
        assert user_updated.role == user_update_dto.role
        assert user_updated.created_at == user_created.created_at

    async def test_invalid_id_should_raise_exception(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
    ):
        user_update_dto = UserUpdateInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )
        user_update_usecase = UserUpdateUseCase(
            fake_user_repository, fake_password_hasher
        )

        with pytest.raises(NotFoundException) as exc:
            await user_update_usecase.execute('random-uuid', user_update_dto)

        assert str(exc.value) == 'Not found'
