class DomainException(Exception):
    """Base exception for domain-related errors."""


class NotFoundException(DomainException):
    """Raised when cannot find a resource."""

    message = 'Not found'

    def __init__(self):
        super().__init__(self.message)


class CannotOperateException(DomainException):
    """Raised when cannot operate over a resource."""

    message = 'Cannot operate: Try again later'

    def __init__(self):
        super().__init__(self.message)


class OperationException(DomainException):
    """Raised when an operation cannot be completed."""

    message = 'Operation failed:'

    def __init__(self, msg: str = ''):
        super().__init__(f'{self.message} {msg}')
