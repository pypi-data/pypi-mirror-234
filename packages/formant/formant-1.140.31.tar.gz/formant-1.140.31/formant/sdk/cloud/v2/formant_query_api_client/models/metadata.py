from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

from ..models.metadata_type import MetadataType

if TYPE_CHECKING:
    from ..models.metadata_tags import MetadataTags


T = TypeVar("T", bound="Metadata")


@attr.s(auto_attribs=True)
class Metadata:
    """
    Attributes:
        device_id (str):
        name (str):
        type (MetadataType):
        tags (MetadataTags):
    """

    device_id: str
    name: str
    type: MetadataType
    tags: "MetadataTags"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        device_id = self.device_id
        name = self.name
        type = self.type.value

        tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deviceId": device_id,
                "name": name,
                "type": type,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata_tags import MetadataTags

        d = src_dict.copy()
        device_id = d.pop("deviceId")

        name = d.pop("name")

        type = MetadataType(d.pop("type"))

        tags = MetadataTags.from_dict(d.pop("tags"))

        metadata = cls(
            device_id=device_id,
            name=name,
            type=type,
            tags=tags,
        )

        metadata.additional_properties = d
        return metadata

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
