from .exceptions import DomainException


class UserAlreadyExistsException(DomainException):
    """Raised when trying to register a user with an existing email."""

    message = 'Email already registered'

    def __init__(self):
        super().__init__(self.message)
