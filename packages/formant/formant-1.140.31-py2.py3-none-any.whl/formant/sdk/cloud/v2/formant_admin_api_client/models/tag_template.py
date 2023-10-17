import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagTemplate")


@attr.s(auto_attribs=True)
class TagTemplate:
    """
    Attributes:
        tag_key (Any):
        organization_id (Union[Unset, str]):
        is_group (Union[Unset, bool]):
        is_telemetry_filter (Union[Unset, bool]):
        is_event_filter (Union[Unset, bool]):
        enabled (Union[Unset, bool]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    tag_key: Any
    organization_id: Union[Unset, str] = UNSET
    is_group: Union[Unset, bool] = UNSET
    is_telemetry_filter: Union[Unset, bool] = UNSET
    is_event_filter: Union[Unset, bool] = UNSET
    enabled: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag_key = self.tag_key
        organization_id = self.organization_id
        is_group = self.is_group
        is_telemetry_filter = self.is_telemetry_filter
        is_event_filter = self.is_event_filter
        enabled = self.enabled
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tagKey": tag_key,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if is_group is not UNSET:
            field_dict["isGroup"] = is_group
        if is_telemetry_filter is not UNSET:
            field_dict["isTelemetryFilter"] = is_telemetry_filter
        if is_event_filter is not UNSET:
            field_dict["isEventFilter"] = is_event_filter
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tag_key = d.pop("tagKey")

        organization_id = d.pop("organizationId", UNSET)

        is_group = d.pop("isGroup", UNSET)

        is_telemetry_filter = d.pop("isTelemetryFilter", UNSET)

        is_event_filter = d.pop("isEventFilter", UNSET)

        enabled = d.pop("enabled", UNSET)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        tag_template = cls(
            tag_key=tag_key,
            organization_id=organization_id,
            is_group=is_group,
            is_telemetry_filter=is_telemetry_filter,
            is_event_filter=is_event_filter,
            enabled=enabled,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        tag_template.additional_properties = d
        return tag_template

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
