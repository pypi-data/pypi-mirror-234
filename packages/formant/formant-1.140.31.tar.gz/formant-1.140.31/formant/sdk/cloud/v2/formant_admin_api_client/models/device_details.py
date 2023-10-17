from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.device_details_type import DeviceDetailsType

if TYPE_CHECKING:
    from ..models.device_details_tags import DeviceDetailsTags


T = TypeVar("T", bound="DeviceDetails")


@attr.s(auto_attribs=True)
class DeviceDetails:
    """
    Attributes:
        id (str):
        name (str):
        type (DeviceDetailsType):
        tags (DeviceDetailsTags):
        enabled (bool):
        public_key (str):
    """

    id: str
    name: str
    type: DeviceDetailsType
    tags: "DeviceDetailsTags"
    enabled: bool
    public_key: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        type = self.type.value

        tags = self.tags.to_dict()

        enabled = self.enabled
        public_key = self.public_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type,
                "tags": tags,
                "enabled": enabled,
                "publicKey": public_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.device_details_tags import DeviceDetailsTags

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        type = DeviceDetailsType(d.pop("type"))

        tags = DeviceDetailsTags.from_dict(d.pop("tags"))

        enabled = d.pop("enabled")

        public_key = d.pop("publicKey")

        device_details = cls(
            id=id,
            name=name,
            type=type,
            tags=tags,
            enabled=enabled,
            public_key=public_key,
        )

        device_details.additional_properties = d
        return device_details

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
