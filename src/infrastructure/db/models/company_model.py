from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Integer, String, Uuid, orm
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.company_type import CompanyType

from ..session import Base


class CompanyModel(Base):
    __tablename__ = 'companies'

    id: Mapped[str] = mapped_column(Uuid, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[CompanyType] = mapped_column(
        Enum(CompanyType), nullable=False
    )
    max_users: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    @orm.validates('max_users')
    def validate_max_users(self, key, value):
        if value is not None and value < 1:
            raise ValueError(
                f'Max users value must be greater than 0, but got {value}'
            )
        return value
