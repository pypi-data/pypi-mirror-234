from enum import Enum


class CountHistoryQueryType(str, Enum):
    DATA_POINT = "data-point"
    BYTE = "byte"
    ASSET_BYTE = "asset-byte"
    ASSET = "asset"
    COST = "cost"

    def __str__(self) -> str:
        return str(self.value)
