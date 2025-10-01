from .exceptions import DomainException


class CompanyAlreadyExistsException(DomainException):
    """Raised when trying to register a company with an existing name."""

    message = 'Name already registered'

    def __init__(self):
        super().__init__(self.message)
