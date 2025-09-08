from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from uuid_extensions import uuid7str


@dataclass
class User:
    name: str
    email: str
    password: str
    id: Optional[str] = field(default_factory=uuid7str)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
