from .exceptions import DomainException


class InvalidCredentialsException(DomainException):
    """Raised when trying to find a non registered or invalid user."""

    message = 'Invalid credentials'

    def __init__(self):
        super().__init__(self.message)


class InvalidTokenException(DomainException):
    """Raised when trying to find a non registered or invalid user."""

    message = 'Invalid token'

    def __init__(self):
        super().__init__(self.message)


class UnauthorizedException(DomainException):
    """Raised when a user is not authorized to access a resource."""

    message = 'Unauthorized'

    def __init__(self, msg=''):
        super().__init__(msg or self.message)
