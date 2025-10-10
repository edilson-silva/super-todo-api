from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.domain.entities.company_entity import Company
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.company_exceptions import (
    CompanyAlreadyRegisteredException,
)
from src.domain.exceptions.exceptions import CannotOperateException
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException
from src.domain.repositories.company_repository import CompanyRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


class AuthSignupUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        company_repo: CompanyRepository,
        password_hasher: PasswordHasher,
    ):
        """
        :param user_repo: UserRepository instance to interact with user.
        :param company_repo: UserRepository instance to interact with company.
        :param password_hasher: PasswordHasher instance to hash user password.
        """
        self.user_repo = user_repo
        self.company_repo = company_repo
        self.password_hasher = password_hasher

    async def execute(self, data: AuthSignupInputDTO):
        """
        Perform signup creating an admin user.

        :param data: The user signup data.

        :return: No response.
        """
        user = await self.user_repo.find_by_email(data.email)

        if user:
            raise UserAlreadyExistsException()

        company = await self.company_repo.find_by_name(data.company_name)

        if company:
            raise CompanyAlreadyRegisteredException()

        company = Company(data.company_name)
        created_company: Company | None = await self.company_repo.create(
            company
        )

        if not created_company:
            raise CannotOperateException()

        hashed_password = await self.password_hasher.async_hash(data.password)
        user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            role=UserRole.ADMIN,
            company_id=created_company.id,
        )

        await self.user_repo.create(user)
