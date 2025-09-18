from typing import List

from ..base_dto import BaseDTO
from .user_output_dto import UserOutputDTO


class UserListOutputDTO(BaseDTO):
    data: List[UserOutputDTO] = []
