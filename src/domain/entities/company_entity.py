from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from uuid_extensions import uuid7

from .base_entity import BaseEntity
from .company_type import CompanyType


@dataclass
class Company(BaseEntity):
    name: str
    type: Optional[CompanyType] = CompanyType.BASIC
    max_users: Optional[int] = 3
    id: Optional[UUID | str | int | bytes] = field(default_factory=uuid7)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
