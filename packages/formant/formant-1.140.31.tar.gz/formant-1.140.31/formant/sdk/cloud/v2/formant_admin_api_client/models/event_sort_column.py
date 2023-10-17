from enum import Enum


class EventSortColumn(str, Enum):
    TYPE = "type"
    MESSAGE = "message"
    DEVICE_NAME = "device.name"
    TIME = "time"

    def __str__(self) -> str:
        return str(self.value)
