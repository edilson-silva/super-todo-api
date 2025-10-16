from fastapi.security import OAuth2PasswordBearer

from src.domain.entities.user_entity import User
from src.domain.exceptions.auth_exceptions import (
    InvalidTokenException,
    UnauthorizedException,
)
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.token_generator import TokenGenerator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/signin')


async def get_requester_from_token(
    token: str,
    token_generator: TokenGenerator,
    user_repository: UserRepository,
) -> User | None:
    """
    Get requester (logged user) based on the token helper.

    :param token: JWT token from the request header.
    :param token_generator: TokenGenerator instance (injected dependency).
    :param user_repository: UserRepository instance (injected dependency).

    :return: The requester user.
    """
    if not token:
        raise InvalidTokenException()

    payload = await token_generator.async_decode(token)

    if not payload:
        raise InvalidTokenException()

    user_id = payload.user_id
    company_id = payload.company_id

    if not all([user_id, company_id]):
        raise InvalidTokenException()

    user = await user_repository.find_by_id(user_id, company_id)

    if not user:
        raise UnauthorizedException()

    return user
