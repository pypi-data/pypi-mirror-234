from enum import Enum


class SimpleForecastCadence(str, Enum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    def __str__(self) -> str:
        return str(self.value)