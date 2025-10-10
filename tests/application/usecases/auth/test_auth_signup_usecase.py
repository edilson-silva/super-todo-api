from datetime import datetime

import pytest

from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.company_exceptions import (
    CompanyAlreadyRegisteredException,
)
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException
from src.domain.repositories.company_repository import CompanyRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestAuthSignupUsecase:
    async def test_new_user_info_should_return_created_user(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository,
        password_hasher: PasswordHasher,
        admin_user_info: dict,
    ):
        signup_dto = AuthSignupInputDTO(
            company_name=admin_user_info['company_name'],
            name=admin_user_info['name'],
            email=admin_user_info['email'],
            password=admin_user_info['password'],
        )
        signup_usecase = AuthSignupUseCase(
            user_repository, company_repository, password_hasher
        )

        response = await signup_usecase.execute(signup_dto)

        assert response is None

        user = await user_repository.find_by_email(signup_dto.email)

        assert user is not None
        assert isinstance(user.id, str)
        assert user.id != ''
        assert user.name == signup_dto.name
        assert user.email == signup_dto.email
        assert user.password != ''
        assert user.role == UserRole.ADMIN
        assert isinstance(user.created_at, datetime)

    async def test_existing_user_should_raise_exception(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository,
        password_hasher: PasswordHasher,
        admin_user: User,
        admin_user_info: dict,
    ):
        signup_dto = AuthSignupInputDTO(
            company_name=admin_user_info['company_name'],
            name=admin_user_info['name'],
            email=admin_user_info['email'],
            password=admin_user_info['password'],
        )
        signup_usecase = AuthSignupUseCase(
            user_repository, company_repository, password_hasher
        )

        with pytest.raises(UserAlreadyExistsException) as exc:
            await signup_usecase.execute(signup_dto)

        assert str(exc.value) == 'Email already registered'

    async def test_already_registered_company_should_raise_exception(
        self,
        user_repository: UserRepository,
        company_repository: CompanyRepository,
        password_hasher: PasswordHasher,
        admin_user: User,
        admin_user_info: dict,
    ):
        signup_dto = AuthSignupInputDTO(
            company_name=admin_user_info['company_name'],
            name=admin_user_info['name'],
            email='new_{}'.format(admin_user_info['email']),
            password=admin_user_info['password'],
        )
        signup_usecase = AuthSignupUseCase(
            user_repository, company_repository, password_hasher
        )

        with pytest.raises(CompanyAlreadyRegisteredException) as exc:
            await signup_usecase.execute(signup_dto)

        assert str(exc.value) == 'Company already registered'
