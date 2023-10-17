from enum import Enum


class AggregateRowType(str, Enum):
    AVG = "avg"
    SUM = "sum"
    COUNT = "count"
    MIN = "min"
    MAX = "max"

    def __str__(self) -> str:
        return str(self.value)
