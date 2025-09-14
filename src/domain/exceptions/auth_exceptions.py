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
