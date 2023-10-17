from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LookerInfo")


@attr.s(auto_attribs=True)
class LookerInfo:
    """
    Attributes:
        looker_group_id (int):
        looker_models (List[str]):
        looker_permissions (List[str]):
        looker_space_id (Union[Unset, float]):
    """

    looker_group_id: int
    looker_models: List[str]
    looker_permissions: List[str]
    looker_space_id: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        looker_group_id = self.looker_group_id
        looker_models = self.looker_models

        looker_permissions = self.looker_permissions

        looker_space_id = self.looker_space_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lookerGroupId": looker_group_id,
                "lookerModels": looker_models,
                "lookerPermissions": looker_permissions,
            }
        )
        if looker_space_id is not UNSET:
            field_dict["lookerSpaceId"] = looker_space_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        looker_group_id = d.pop("lookerGroupId")

        looker_models = cast(List[str], d.pop("lookerModels"))

        looker_permissions = cast(List[str], d.pop("lookerPermissions"))

        looker_space_id = d.pop("lookerSpaceId", UNSET)

        looker_info = cls(
            looker_group_id=looker_group_id,
            looker_models=looker_models,
            looker_permissions=looker_permissions,
            looker_space_id=looker_space_id,
        )

        looker_info.additional_properties = d
        return looker_info

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
