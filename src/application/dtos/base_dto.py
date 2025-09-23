from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # allow building from dataclasses/ORM
    )

    @classmethod
    def model_validate(cls, obj):
        # Convert all UUID properties to strings
        for attr, value in vars(obj).items():
            if isinstance(value, UUID):
                setattr(obj, attr, str(value))

        return super().model_validate(obj)
