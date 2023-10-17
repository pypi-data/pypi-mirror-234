import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_command_template_parameter_meta import PartialCommandTemplateParameterMeta
    from ..models.partial_command_template_tags import PartialCommandTemplateTags
    from ..models.scope_filter import ScopeFilter


T = TypeVar("T", bound="PartialCommandTemplate")


@attr.s(auto_attribs=True)
class PartialCommandTemplate:
    """
    Attributes:
        organization_id (Union[Unset, str]):
        name (Union[Unset, str]):
        command (Union[Unset, str]):
        description (Union[Unset, str]):
        parameter_enabled (Union[Unset, bool]):
        parameter_value (Union[Unset, str]):
        parameter_meta (Union[Unset, PartialCommandTemplateParameterMeta]):
        device_scope (Union[Unset, None, ScopeFilter]):
        enabled (Union[Unset, bool]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, PartialCommandTemplateTags]):
    """

    organization_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    command: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    parameter_enabled: Union[Unset, bool] = UNSET
    parameter_value: Union[Unset, str] = UNSET
    parameter_meta: Union[Unset, "PartialCommandTemplateParameterMeta"] = UNSET
    device_scope: Union[Unset, None, "ScopeFilter"] = UNSET
    enabled: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "PartialCommandTemplateTags"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        organization_id = self.organization_id
        name = self.name
        command = self.command
        description = self.description
        parameter_enabled = self.parameter_enabled
        parameter_value = self.parameter_value
        parameter_meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameter_meta, Unset):
            parameter_meta = self.parameter_meta.to_dict()

        device_scope: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.device_scope, Unset):
            device_scope = self.device_scope.to_dict() if self.device_scope else None

        enabled = self.enabled
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if name is not UNSET:
            field_dict["name"] = name
        if command is not UNSET:
            field_dict["command"] = command
        if description is not UNSET:
            field_dict["description"] = description
        if parameter_enabled is not UNSET:
            field_dict["parameterEnabled"] = parameter_enabled
        if parameter_value is not UNSET:
            field_dict["parameterValue"] = parameter_value
        if parameter_meta is not UNSET:
            field_dict["parameterMeta"] = parameter_meta
        if device_scope is not UNSET:
            field_dict["deviceScope"] = device_scope
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.partial_command_template_parameter_meta import PartialCommandTemplateParameterMeta
        from ..models.partial_command_template_tags import PartialCommandTemplateTags
        from ..models.scope_filter import ScopeFilter

        d = src_dict.copy()
        organization_id = d.pop("organizationId", UNSET)

        name = d.pop("name", UNSET)

        command = d.pop("command", UNSET)

        description = d.pop("description", UNSET)

        parameter_enabled = d.pop("parameterEnabled", UNSET)

        parameter_value = d.pop("parameterValue", UNSET)

        _parameter_meta = d.pop("parameterMeta", UNSET)
        parameter_meta: Union[Unset, PartialCommandTemplateParameterMeta]
        if isinstance(_parameter_meta, Unset):
            parameter_meta = UNSET
        else:
            parameter_meta = PartialCommandTemplateParameterMeta.from_dict(_parameter_meta)

        _device_scope = d.pop("deviceScope", UNSET)
        device_scope: Union[Unset, None, ScopeFilter]
        if _device_scope is None:
            device_scope = None
        elif isinstance(_device_scope, Unset):
            device_scope = UNSET
        else:
            device_scope = ScopeFilter.from_dict(_device_scope)

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

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PartialCommandTemplateTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PartialCommandTemplateTags.from_dict(_tags)

        partial_command_template = cls(
            organization_id=organization_id,
            name=name,
            command=command,
            description=description,
            parameter_enabled=parameter_enabled,
            parameter_value=parameter_value,
            parameter_meta=parameter_meta,
            device_scope=device_scope,
            enabled=enabled,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
        )

        partial_command_template.additional_properties = d
        return partial_command_template

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
