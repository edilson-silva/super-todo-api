from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
)
from src.infrastructure.security.password_hasher_bcrypt import (
    PasswordHasherBcrypt,
)
from src.infrastructure.security.token_generator_pyjwt import (
    TokenGeneratorPyJWT,
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


def get_token_generator() -> TokenGenerator:
    """
    Dependency to get a TokenGenerator instance.

    :return: An instance of TokenGenerator.
    """
    return TokenGeneratorPyJWT()


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


def get_auth_signin_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_generator: TokenGenerator = Depends(get_token_generator),
) -> AuthSigninUseCase:
    """
    Dependency to get an AuthSigninUseCase instance.

    :param repository: UserRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of AuthSigninUseCase.
    """
    return AuthSigninUseCase(repository, password_hasher, token_generator)


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


def get_user_get_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserGetUseCase:
    """
    Dependency to get a UserGetUseCase instance.

    :param repository: UserRepository dependency.

    :return: An instance of UserGetUseCase.
    """
    return UserGetUseCase(repository)


def get_user_list_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserGetUseCase:
    """
    Dependency to get a UserListUseCase instance.

    :param repository: UserRepository dependency.

    :return: An instance of UserListUseCase.
    """
    return UserListUseCase(repository)


AuthSignupUseCaseDep = Depends(get_auth_signup_use_case)
AuthSigninUseCaseDep = Depends(get_auth_signin_use_case)
UserCreateUseCaseDep = Depends(get_user_create_use_case)
UserGetUseCaseDep = Depends(get_user_get_use_case)
UserListUseCaseDep = Depends(get_user_list_use_case)
