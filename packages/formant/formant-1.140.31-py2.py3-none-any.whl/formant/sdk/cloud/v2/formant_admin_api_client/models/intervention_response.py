import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.intervention_response_intervention_type import InterventionResponseInterventionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InterventionResponse")


@attr.s(auto_attribs=True)
class InterventionResponse:
    """
    Attributes:
        intervention_type (InterventionResponseInterventionType):
        data (Any):
        intervention_id (str):
        user_id (Union[Unset, str]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    intervention_type: InterventionResponseInterventionType
    data: Any
    intervention_id: str
    user_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        intervention_type = self.intervention_type.value

        data = self.data
        intervention_id = self.intervention_id
        user_id = self.user_id
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
                "interventionType": intervention_type,
                "data": data,
                "interventionId": intervention_id,
            }
        )
        if user_id is not UNSET:
            field_dict["userId"] = user_id
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
        intervention_type = InterventionResponseInterventionType(d.pop("interventionType"))

        data = d.pop("data")

        intervention_id = d.pop("interventionId")

        user_id = d.pop("userId", UNSET)

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

        intervention_response = cls(
            intervention_type=intervention_type,
            data=data,
            intervention_id=intervention_id,
            user_id=user_id,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        intervention_response.additional_properties = d
        return intervention_response

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
