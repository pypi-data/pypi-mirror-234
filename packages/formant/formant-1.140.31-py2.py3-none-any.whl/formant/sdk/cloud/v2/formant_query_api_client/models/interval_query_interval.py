from enum import Enum


class IntervalQueryInterval(str, Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)
