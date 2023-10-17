import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.device_query_type import DeviceQueryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeviceQuery")


@attr.s(auto_attribs=True)
class DeviceQuery:
    """
    Attributes:
        name (Union[Unset, str]):
        query (Union[Unset, str]):
        tags (Union[Unset, Any]):
        fleet_id (Union[Unset, None, str]):
        enabled (Union[Unset, bool]):
        fully_configured (Union[Unset, bool]):
        type (Union[Unset, DeviceQueryType]):
        count (Union[Unset, float]):
        offset (Union[Unset, float]):
        disabled_before (Union[Unset, datetime.datetime]):
    """

    name: Union[Unset, str] = UNSET
    query: Union[Unset, str] = UNSET
    tags: Union[Unset, Any] = UNSET
    fleet_id: Union[Unset, None, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    fully_configured: Union[Unset, bool] = UNSET
    type: Union[Unset, DeviceQueryType] = UNSET
    count: Union[Unset, float] = UNSET
    offset: Union[Unset, float] = UNSET
    disabled_before: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        query = self.query
        tags = self.tags
        fleet_id = self.fleet_id
        enabled = self.enabled
        fully_configured = self.fully_configured
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        count = self.count
        offset = self.offset
        disabled_before: Union[Unset, str] = UNSET
        if not isinstance(self.disabled_before, Unset):
            disabled_before = self.disabled_before.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if query is not UNSET:
            field_dict["query"] = query
        if tags is not UNSET:
            field_dict["tags"] = tags
        if fleet_id is not UNSET:
            field_dict["fleetId"] = fleet_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if fully_configured is not UNSET:
            field_dict["fullyConfigured"] = fully_configured
        if type is not UNSET:
            field_dict["type"] = type
        if count is not UNSET:
            field_dict["count"] = count
        if offset is not UNSET:
            field_dict["offset"] = offset
        if disabled_before is not UNSET:
            field_dict["disabledBefore"] = disabled_before

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        query = d.pop("query", UNSET)

        tags = d.pop("tags", UNSET)

        fleet_id = d.pop("fleetId", UNSET)

        enabled = d.pop("enabled", UNSET)

        fully_configured = d.pop("fullyConfigured", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, DeviceQueryType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DeviceQueryType(_type)

        count = d.pop("count", UNSET)

        offset = d.pop("offset", UNSET)

        _disabled_before = d.pop("disabledBefore", UNSET)
        disabled_before: Union[Unset, datetime.datetime]
        if isinstance(_disabled_before, Unset):
            disabled_before = UNSET
        else:
            disabled_before = isoparse(_disabled_before)

        device_query = cls(
            name=name,
            query=query,
            tags=tags,
            fleet_id=fleet_id,
            enabled=enabled,
            fully_configured=fully_configured,
            type=type,
            count=count,
            offset=offset,
            disabled_before=disabled_before,
        )

        device_query.additional_properties = d
        return device_query

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
