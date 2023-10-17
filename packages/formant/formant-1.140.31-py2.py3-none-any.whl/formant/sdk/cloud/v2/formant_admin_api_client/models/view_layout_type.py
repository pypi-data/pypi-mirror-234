from enum import Enum


class ViewLayoutType(str, Enum):
    OBSERVE = "observe"
    FULLSCREEN = "fullscreen"
    ANALYTICS = "analytics"
    TELEOP = "teleop"

    def __str__(self) -> str:
        return str(self.value)
