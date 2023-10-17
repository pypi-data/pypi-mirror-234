from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskReportColumn")


@attr.s(auto_attribs=True)
class TaskReportColumn:
    """
    Attributes:
        table_name (str):
        name (str):
        columns (List[Any]):
        y_axis (Union[Unset, str]):
        device_ids (Union[Unset, List[Any]]):
    """

    table_name: str
    name: str
    columns: List[Any]
    y_axis: Union[Unset, str] = UNSET
    device_ids: Union[Unset, List[Any]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        table_name = self.table_name
        name = self.name
        columns = self.columns

        y_axis = self.y_axis
        device_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.device_ids, Unset):
            device_ids = self.device_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tableName": table_name,
                "name": name,
                "columns": columns,
            }
        )
        if y_axis is not UNSET:
            field_dict["yAxis"] = y_axis
        if device_ids is not UNSET:
            field_dict["deviceIds"] = device_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        table_name = d.pop("tableName")

        name = d.pop("name")

        columns = cast(List[Any], d.pop("columns"))

        y_axis = d.pop("yAxis", UNSET)

        device_ids = cast(List[Any], d.pop("deviceIds", UNSET))

        task_report_column = cls(
            table_name=table_name,
            name=name,
            columns=columns,
            y_axis=y_axis,
            device_ids=device_ids,
        )

        task_report_column.additional_properties = d
        return task_report_column

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
