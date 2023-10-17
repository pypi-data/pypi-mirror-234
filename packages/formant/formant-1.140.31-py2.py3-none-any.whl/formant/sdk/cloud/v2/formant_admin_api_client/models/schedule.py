import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.schedule_type import ScheduleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Schedule")


@attr.s(auto_attribs=True)
class Schedule:
    """
    Attributes:
        name (str):
        description (str):
        type (ScheduleType):
        duration_ms (int):
        timezone (str):
        device_id (str):
        status (str):
        organization_id (Union[Unset, str]):
        at (Optional[datetime.datetime]):
        cron (Optional[str]):
        command_template_id (Optional[str]):
        parameter_value (Optional[str]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    name: str
    description: str
    type: ScheduleType
    duration_ms: int
    timezone: str
    device_id: str
    status: str
    at: Optional[datetime.datetime]
    cron: Optional[str]
    command_template_id: Optional[str]
    parameter_value: Optional[str]
    organization_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type = self.type.value

        duration_ms = self.duration_ms
        timezone = self.timezone
        device_id = self.device_id
        status = self.status
        organization_id = self.organization_id
        at = self.at.isoformat() if self.at else None

        cron = self.cron
        command_template_id = self.command_template_id
        parameter_value = self.parameter_value
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
                "name": name,
                "description": description,
                "type": type,
                "durationMs": duration_ms,
                "timezone": timezone,
                "deviceId": device_id,
                "status": status,
                "at": at,
                "cron": cron,
                "commandTemplateId": command_template_id,
                "parameterValue": parameter_value,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
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
        name = d.pop("name")

        description = d.pop("description")

        type = ScheduleType(d.pop("type"))

        duration_ms = d.pop("durationMs")

        timezone = d.pop("timezone")

        device_id = d.pop("deviceId")

        status = d.pop("status")

        organization_id = d.pop("organizationId", UNSET)

        _at = d.pop("at")
        at: Optional[datetime.datetime]
        if _at is None:
            at = None
        else:
            at = isoparse(_at)

        cron = d.pop("cron")

        command_template_id = d.pop("commandTemplateId")

        parameter_value = d.pop("parameterValue")

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

        schedule = cls(
            name=name,
            description=description,
            type=type,
            duration_ms=duration_ms,
            timezone=timezone,
            device_id=device_id,
            status=status,
            organization_id=organization_id,
            at=at,
            cron=cron,
            command_template_id=command_template_id,
            parameter_value=parameter_value,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        schedule.additional_properties = d
        return schedule

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
