from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class BaseEntity:
    def __post_init__(self):
        for attr, value in vars(self).items():
            # Set all datetime properties timezone to utc
            if isinstance(value, datetime):
                if value.tzinfo is None:
                    setattr(self, attr, value.replace(tzinfo=timezone.utc))
