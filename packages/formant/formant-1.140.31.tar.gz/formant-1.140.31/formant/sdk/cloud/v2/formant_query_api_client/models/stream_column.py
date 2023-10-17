from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.stream_column_aggregate_type import StreamColumnAggregateType
from ..models.stream_column_stream_type import StreamColumnStreamType
from ..types import UNSET, Unset

T = TypeVar("T", bound="StreamColumn")


@attr.s(auto_attribs=True)
class StreamColumn:
    """
    Attributes:
        stream_name (str):
        stream_type (StreamColumnStreamType):
        aggregate_type (Union[Unset, StreamColumnAggregateType]):
    """

    stream_name: str
    stream_type: StreamColumnStreamType
    aggregate_type: Union[Unset, StreamColumnAggregateType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        stream_name = self.stream_name
        stream_type = self.stream_type.value

        aggregate_type: Union[Unset, str] = UNSET
        if not isinstance(self.aggregate_type, Unset):
            aggregate_type = self.aggregate_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "streamName": stream_name,
                "streamType": stream_type,
            }
        )
        if aggregate_type is not UNSET:
            field_dict["aggregateType"] = aggregate_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        stream_name = d.pop("streamName")

        stream_type = StreamColumnStreamType(d.pop("streamType"))

        _aggregate_type = d.pop("aggregateType", UNSET)
        aggregate_type: Union[Unset, StreamColumnAggregateType]
        if isinstance(_aggregate_type, Unset):
            aggregate_type = UNSET
        else:
            aggregate_type = StreamColumnAggregateType(_aggregate_type)

        stream_column = cls(
            stream_name=stream_name,
            stream_type=stream_type,
            aggregate_type=aggregate_type,
        )

        stream_column.additional_properties = d
        return stream_column

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
