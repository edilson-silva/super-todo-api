from datetime import datetime

import pytest

from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_singup_usecase import AuthSignupUseCase
from src.domain.entities.user_role import UserRole
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestAuthSignupUsecase:
    async def test_new_user_should_be_created(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
    ):
        signup_dto = AuthSignupInputDTO(
            name='Test User',
            email='test@example.com',
            password='123456789',
        )
        signup_usecase = AuthSignupUseCase(
            fake_user_repository, fake_password_hasher
        )

        response = await signup_usecase.execute(signup_dto)

        assert response is None

        user = await fake_user_repository.find_by_email(signup_dto.email)

        assert user is not None
        assert isinstance(user.id, str)
        assert user.id != ''
        assert user.name == signup_dto.name
        assert user.email == signup_dto.email
        assert user.password == f'hashed_{signup_dto.password}'
        assert user.role == UserRole.ADMIN
        assert isinstance(user.created_at, datetime)
