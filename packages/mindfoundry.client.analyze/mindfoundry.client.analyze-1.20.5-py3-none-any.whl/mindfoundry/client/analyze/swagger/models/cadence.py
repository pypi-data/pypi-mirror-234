from enum import Enum


class Cadence(str, Enum):
    DAILY = "DAILY"
    HOURLY = "HOURLY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    BUSINESS_DAILY = "BUSINESS_DAILY"

    def __str__(self) -> str:
        return str(self.value)