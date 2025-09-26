from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # allow building from dataclasses/ORM
    )

    @classmethod
    def model_validate(cls, obj):
        for attr, value in vars(obj).items():
            # Convert all UUID properties to strings
            if isinstance(value, UUID):
                setattr(obj, attr, str(value))

            # Set all datetime properties timezone to utc
            if isinstance(value, datetime):
                if value.tzinfo is None:
                    setattr(obj, attr, value.replace(tzinfo=timezone.utc))

        return super().model_validate(obj)
