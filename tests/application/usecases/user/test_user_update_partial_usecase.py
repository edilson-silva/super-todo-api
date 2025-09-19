import pytest

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.dtos.user.user_update_partial_dto import (
    UserUpdatePartialInputDTO,
    UserUpdatePartialOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_update_partial_usecase import (
    UserUpdatePartialUseCase,
)
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserUpdatePartialUsecase:
    user_create_dto = UserCreateInputDTO(
        name='Test User',
        email='test@example.com',
        password='123456789',
    )

    async def test_valid_id_with_new_name_should_return_updated_user_info(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
    ):
        user_create_usecase = UserCreateUseCase(
            fake_user_repository, fake_password_hasher
        )

        user_created = await user_create_usecase.execute(self.user_create_dto)

        user_update_partial_dto = UserUpdatePartialInputDTO(
            name='Updated Name',
        )
        user_update_partial_usecase = UserUpdatePartialUseCase(
            fake_user_repository, fake_password_hasher
        )

        user_updated = await user_update_partial_usecase.execute(
            user_created.id, user_update_partial_dto
        )

        print(user_created)

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_update_partial_dto.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_created.avatar
        assert user_updated.role == user_created.role
        assert user_updated.created_at == user_created.created_at
