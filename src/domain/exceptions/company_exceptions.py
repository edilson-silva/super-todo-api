from .exceptions import DomainException


class CompanyAlreadyRegisteredException(DomainException):
    """Raised when trying to register a company with an existing name."""

    message = 'Company already registered'

    def __init__(self):
        super().__init__(self.message)
