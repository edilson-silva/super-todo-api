from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_delete_usecase import UserDeleteUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.application.usecases.user.user_update_partial_usecase import (
    UserUpdatePartialUseCase,
)
from src.application.usecases.user.user_update_usecase import UserUpdateUseCase
from src.domain.repositories.company_repository import CompanyRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.company_repository_sqlalchemy import (
    CompanyRepositorySQLAlchemy,
)
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


def get_company_repository(
    db: AsyncGenerator[AsyncSession, None] = Depends(get_db),
) -> CompanyRepository:
    """
    Dependency to get a CompanyRepository instance.

    :param db: Database session dependency.

    :return: An instance of CompanyRepository.
    """
    return CompanyRepositorySQLAlchemy(session=db)


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
    user_repository: UserRepository = Depends(get_user_repository),
    company_repository: CompanyRepository = Depends(get_company_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthSignupUseCase:
    """
    Dependency to get an AuthSignupUseCase instance.

    :param user_repository: UserRepository dependency.
    :param company_repository: CompanyRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of AuthSignupUseCase.
    """
    return AuthSignupUseCase(
        user_repository, company_repository, password_hasher
    )


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
) -> UserListUseCase:
    """
    Dependency to get a UserListUseCase instance.

    :param repository: UserRepository dependency.

    :return: An instance of UserListUseCase.
    """
    return UserListUseCase(repository)


def get_user_delete_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> UserDeleteUseCase:
    """
    Dependency to get a UserDeleteUseCase instance.

    :param repository: UserRepository dependency.

    :return: An instance of UserDeleteUseCase.
    """
    return UserDeleteUseCase(repository)


def get_user_update_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> UserUpdateUseCase:
    """
    Dependency to get a UserUpdateUseCase instance.

    :param repository: UserRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of UserUpdateUseCase.
    """
    return UserUpdateUseCase(repository, password_hasher)


def get_user_update_partial_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> UserUpdatePartialUseCase:
    """
    Dependency to get a UserUpdatePartialUseCase instance.

    :param repository: UserRepository dependency.
    :param password_hasher: PasswordHasher dependency.

    :return: An instance of UserUpdatePartialUseCase.
    """
    return UserUpdatePartialUseCase(repository, password_hasher)


AuthSignupUseCaseDep = Depends(get_auth_signup_use_case)
AuthSigninUseCaseDep = Depends(get_auth_signin_use_case)
UserCreateUseCaseDep = Depends(get_user_create_use_case)
UserGetUseCaseDep = Depends(get_user_get_use_case)
UserListUseCaseDep = Depends(get_user_list_use_case)
UserDeleteUseCaseDep = Depends(get_user_delete_use_case)
UserUpdateUseCaseDep = Depends(get_user_update_use_case)
UserUpdatePartialUseCaseDep = Depends(get_user_update_partial_use_case)
