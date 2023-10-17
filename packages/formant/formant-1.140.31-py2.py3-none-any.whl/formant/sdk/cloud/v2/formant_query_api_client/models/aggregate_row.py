from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aggregate_row_type import AggregateRowType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AggregateRow")


@attr.s(auto_attribs=True)
class AggregateRow:
    """
    Attributes:
        name (str):
        stream_name (str):
        value (float):
        type (AggregateRowType):
        unit (Union[Unset, str]):
        label (Union[Unset, str]):
    """

    name: str
    stream_name: str
    value: float
    type: AggregateRowType
    unit: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        stream_name = self.stream_name
        value = self.value
        type = self.type.value

        unit = self.unit
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "streamName": stream_name,
                "value": value,
                "type": type,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        stream_name = d.pop("streamName")

        value = d.pop("value")

        type = AggregateRowType(d.pop("type"))

        unit = d.pop("unit", UNSET)

        label = d.pop("label", UNSET)

        aggregate_row = cls(
            name=name,
            stream_name=stream_name,
            value=value,
            type=type,
            unit=unit,
            label=label,
        )

        aggregate_row.additional_properties = d
        return aggregate_row

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
