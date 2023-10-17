import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.count_history_query_type import CountHistoryQueryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CountHistoryQuery")


@attr.s(auto_attribs=True)
class CountHistoryQuery:
    """
    Attributes:
        type (CountHistoryQueryType):
        start (datetime.datetime):
        end (datetime.datetime):
        organization_id (Union[Unset, str]):
    """

    type: CountHistoryQueryType
    start: datetime.datetime
    end: datetime.datetime
    organization_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        start = self.start.isoformat()

        end = self.end.isoformat()

        organization_id = self.organization_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "start": start,
                "end": end,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = CountHistoryQueryType(d.pop("type"))

        start = isoparse(d.pop("start"))

        end = isoparse(d.pop("end"))

        organization_id = d.pop("organizationId", UNSET)

        count_history_query = cls(
            type=type,
            start=start,
            end=end,
            organization_id=organization_id,
        )

        count_history_query.additional_properties = d
        return count_history_query

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
