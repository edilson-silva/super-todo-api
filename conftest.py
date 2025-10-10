from collections.abc import AsyncGenerator
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
    TokenGeneratorEncodeOutputDTO,
)
from src.domain.entities.company_entity import Company
from src.domain.entities.user_entity import User, UserRole
from src.domain.repositories.company_repository import CompanyRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator
from src.infrastructure.db.session import Base, get_db
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
from src.main import app


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return PasswordHasherBcrypt()


@pytest.fixture
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')

    AsyncSesssionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSesssionLocal() as session:
        yield session

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def user_repository(
    get_db_session,
) -> UserRepository:
    return UserRepositorySQLAlchemy(get_db_session)


@pytest.fixture
async def company_repository(
    get_db_session,
) -> CompanyRepository:
    return CompanyRepositorySQLAlchemy(get_db_session)


@pytest.fixture
def token_generator() -> TokenGenerator:
    return TokenGeneratorPyJWT()


@pytest.fixture
def admin_user_info():
    return {
        'name': 'admin',
        'email': 'admin@example.com',
        'password': '123456789',
        'role': UserRole.ADMIN,
        'company_name': 'company',
    }


@pytest.fixture
def basic_user_info():
    return {
        'name': 'basic',
        'email': 'basic@example.com',
        'password': '123456789',
        'role': UserRole.USER,
        'company_name': 'company',
    }


@pytest.fixture
async def admin_user(
    user_repository: UserRepository,
    company_repository: CompanyRepository,
    password_hasher: PasswordHasher,
    admin_user_info: dict,
) -> User:
    company = Company(name='Test Company')
    company = await company_repository.create(company)

    user_password_hashed = await password_hasher.async_hash(
        admin_user_info['password']
    )

    user = User(
        name=admin_user_info['name'],
        email=admin_user_info['email'],
        password=user_password_hashed,
        role=admin_user_info['role'],
        company_id=str(company.id),
    )

    user = await user_repository.create(user)

    return user


@pytest.fixture
async def basic_user(
    user_repository: UserRepository,
    company_repository: CompanyRepository,
    password_hasher: PasswordHasher,
    basic_user_info: dict,
) -> User:
    company = Company(name='Test Company')
    company = await company_repository.create(company)

    user_password_hashed = await password_hasher.async_hash(
        basic_user_info['password']
    )

    user = User(
        name=basic_user_info['name'],
        email=basic_user_info['email'],
        password=user_password_hashed,
        role=basic_user_info['role'],
        company_id=str(company.id),
    )

    user = await user_repository.create(user)

    return user


@pytest.fixture
async def admin_user_token(
    token_generator: TokenGenerator, admin_user: User
) -> TokenGeneratorEncodeOutputDTO:
    token_generator_encode_input_dto = TokenGeneratorEncodeInputDTO(
        user_id=str(admin_user.id),
        user_role=UserRole(admin_user.role),
        company_id=str(admin_user.company_id),
    )
    token = await token_generator.async_encode(
        token_generator_encode_input_dto
    )

    return token


@pytest.fixture
async def basic_user_token(
    token_generator: TokenGenerator, basic_user: User
) -> TokenGeneratorEncodeOutputDTO:
    token_generator_encode_input_dto = TokenGeneratorEncodeInputDTO(
        user_id=str(basic_user.id),
        user_role=UserRole(basic_user.role),
        company_id=str(basic_user.company_id),
    )
    token = await token_generator.async_encode(
        token_generator_encode_input_dto
    )

    return token


@pytest.fixture
async def client(get_db_session) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db_session():
        yield get_db_session

    app.dependency_overrides[get_db] = override_get_db_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url='http://test', follow_redirects=True
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def datetime_to_web_iso():
    def convert_date(date: datetime) -> str:
        return date.isoformat().replace('+00:00', 'Z')

    return convert_date
