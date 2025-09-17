from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from uuid_extensions import uuid7str

from .user_role import UserRole


@dataclass
class User:
    name: str
    email: str
    password: str
    role: Optional[UserRole]
    id: Optional[str] = field(default_factory=uuid7str)
    avatar: Optional[str] = ''
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
