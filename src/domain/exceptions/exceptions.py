class DomainException(Exception):
    """Base exception for domain-related errors."""


class NotFoundException(DomainException):
    """Raised when cannot find a resource."""

    message = 'Not found'

    def __init__(self):
        super().__init__(self.message)
