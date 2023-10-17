from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.count_history_entry import CountHistoryEntry


T = TypeVar("T", bound="CountHistory")


@attr.s(auto_attribs=True)
class CountHistory:
    """
    Attributes:
        total (int):
        counts (List['CountHistoryEntry']):
    """

    total: int
    counts: List["CountHistoryEntry"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total = self.total
        counts = []
        for counts_item_data in self.counts:
            counts_item = counts_item_data.to_dict()

            counts.append(counts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "counts": counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.count_history_entry import CountHistoryEntry

        d = src_dict.copy()
        total = d.pop("total")

        counts = []
        _counts = d.pop("counts")
        for counts_item_data in _counts:
            counts_item = CountHistoryEntry.from_dict(counts_item_data)

            counts.append(counts_item)

        count_history = cls(
            total=total,
            counts=counts,
        )

        count_history.additional_properties = d
        return count_history

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
