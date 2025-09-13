from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases.auth.auth_login_usecase import AuthLoginUseCase
from src.application.usecases.auth.auth_singup_usecase import AuthSignupUseCase
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
)
from src.infrastructure.security.password_hasher_bcrypt import (
    PasswordHasherBcrypt,
)


def get_user_repository(
    db: AsyncGenerator[AsyncSession, None] = Depends(get_db),
) -> UserRepository:
    """
    Dependency to get a UserRepository instance.

    :param db: Database session dependency.

    :return: An instance of UserRepository.
    """
    return UserRepositorySQLAlchemy(session=db)


def get_password_hasher() -> PasswordHasher:
    """
    Dependency to get a PasswordHasher instance.

    :return: An instance of PasswordHasher.
    """
    return PasswordHasherBcrypt()


def get_auth_signup_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthSignupUseCase:
    """
    Dependency to get an AuthSignupUseCase instance.

    :param repository: UserRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of AuthSignupUseCase.
    """
    return AuthSignupUseCase(repository, password_hasher)


def get_auth_login_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthLoginUseCase:
    """
    Dependency to get an AuthLoginUseCase instance.

    :param repository: UserRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of AuthLoginUseCase.
    """
    return AuthLoginUseCase(repository, password_hasher)


def get_user_create_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> UserCreateUseCase:
    """
    Dependency to get a UserCreateUseCase instance.

    :param repository: UserRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of UserCreateUseCase.
    """
    return UserCreateUseCase(repository, password_hasher)


AuthSignupUseCaseDep = Depends(get_auth_signup_use_case)
AuthLoginUseCaseDep = Depends(get_auth_login_use_case)
UserCreateUseCaseDep = Depends(get_user_create_use_case)
