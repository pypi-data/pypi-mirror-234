import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="CountHistoryEntryCount")


@attr.s(auto_attribs=True)
class CountHistoryEntryCount:
    """
    Attributes:
        field_0 (datetime.datetime):
        field_1 (int):
    """

    field_0: datetime.datetime
    field_1: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_0 = self.field_0.isoformat()

        field_1 = self.field_1

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "0": field_0,
                "1": field_1,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_0 = isoparse(d.pop("0"))

        field_1 = d.pop("1")

        count_history_entry_count = cls(
            field_0=field_0,
            field_1=field_1,
        )

        count_history_entry_count.additional_properties = d
        return count_history_entry_count

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
