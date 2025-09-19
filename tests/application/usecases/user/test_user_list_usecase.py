import pytest

from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.domain.repositories.user_repository import UserRepository


@pytest.mark.asyncio
class TestUserListUsecase:
    async def test_should_return_an_empty_list(
        self,
        fake_user_repository: UserRepository,
    ):
        user_list_usecase = UserListUseCase(fake_user_repository)

        users = await user_list_usecase.execute()

        assert isinstance(users, UserListOutputDTO)
        assert users.data == []
