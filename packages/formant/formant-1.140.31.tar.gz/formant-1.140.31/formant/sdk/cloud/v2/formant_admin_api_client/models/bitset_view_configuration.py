from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BitsetViewConfiguration")


@attr.s(auto_attribs=True)
class BitsetViewConfiguration:
    """
    Attributes:
        split_by_key (Union[Unset, str]):
    """

    split_by_key: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        split_by_key = self.split_by_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if split_by_key is not UNSET:
            field_dict["splitByKey"] = split_by_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        split_by_key = d.pop("splitByKey", UNSET)

        bitset_view_configuration = cls(
            split_by_key=split_by_key,
        )

        bitset_view_configuration.additional_properties = d
        return bitset_view_configuration

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
