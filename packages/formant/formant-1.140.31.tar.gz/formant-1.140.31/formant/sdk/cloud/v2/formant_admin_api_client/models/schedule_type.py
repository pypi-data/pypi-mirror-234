from enum import Enum


class ScheduleType(str, Enum):
    COMMAND = "command"

    def __str__(self) -> str:
        return str(self.value)
