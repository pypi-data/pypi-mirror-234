import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.sql_query_aggregate_level import SqlQueryAggregateLevel
from ..models.sql_query_types_item import SqlQueryTypesItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stream_column import StreamColumn
    from ..models.task_report_column import TaskReportColumn


T = TypeVar("T", bound="SqlQuery")


@attr.s(auto_attribs=True)
class SqlQuery:
    """
    Attributes:
        sql_query (Union[Unset, str]):
        parameters (Union[Unset, List[str]]):
        start (Union[Unset, datetime.datetime]):
        end (Union[Unset, datetime.datetime]):
        limit (Union[Unset, float]):
        stream_columns (Union[Unset, List['StreamColumn']]):
        task_columns (Union[Unset, List['TaskReportColumn']]):
        aggregate_level (Union[Unset, SqlQueryAggregateLevel]):
        order_by_column (Union[Unset, str]):
        order_by_descending (Union[Unset, bool]):
        visible_columns (Union[Unset, List[str]]):
        group_by_device (Union[Unset, bool]):
        type (Union[Unset, str]):
        unit (Union[Unset, str]):
        device_ids (Union[Unset, List[str]]):
        names (Union[Unset, List[str]]):
        types (Union[Unset, List[SqlQueryTypesItem]]):
        tags (Union[Unset, Any]):
        not_names (Union[Unset, List[str]]):
        agent_ids (Union[Unset, List[str]]):
    """

    sql_query: Union[Unset, str] = UNSET
    parameters: Union[Unset, List[str]] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    end: Union[Unset, datetime.datetime] = UNSET
    limit: Union[Unset, float] = UNSET
    stream_columns: Union[Unset, List["StreamColumn"]] = UNSET
    task_columns: Union[Unset, List["TaskReportColumn"]] = UNSET
    aggregate_level: Union[Unset, SqlQueryAggregateLevel] = UNSET
    order_by_column: Union[Unset, str] = UNSET
    order_by_descending: Union[Unset, bool] = UNSET
    visible_columns: Union[Unset, List[str]] = UNSET
    group_by_device: Union[Unset, bool] = UNSET
    type: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    device_ids: Union[Unset, List[str]] = UNSET
    names: Union[Unset, List[str]] = UNSET
    types: Union[Unset, List[SqlQueryTypesItem]] = UNSET
    tags: Union[Unset, Any] = UNSET
    not_names: Union[Unset, List[str]] = UNSET
    agent_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sql_query = self.sql_query
        parameters: Union[Unset, List[str]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        end: Union[Unset, str] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.isoformat()

        limit = self.limit
        stream_columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.stream_columns, Unset):
            stream_columns = []
            for stream_columns_item_data in self.stream_columns:
                stream_columns_item = stream_columns_item_data.to_dict()

                stream_columns.append(stream_columns_item)

        task_columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.task_columns, Unset):
            task_columns = []
            for task_columns_item_data in self.task_columns:
                task_columns_item = task_columns_item_data.to_dict()

                task_columns.append(task_columns_item)

        aggregate_level: Union[Unset, str] = UNSET
        if not isinstance(self.aggregate_level, Unset):
            aggregate_level = self.aggregate_level.value

        order_by_column = self.order_by_column
        order_by_descending = self.order_by_descending
        visible_columns: Union[Unset, List[str]] = UNSET
        if not isinstance(self.visible_columns, Unset):
            visible_columns = self.visible_columns

        group_by_device = self.group_by_device
        type = self.type
        unit = self.unit
        device_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.device_ids, Unset):
            device_ids = self.device_ids

        names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names

        types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.types, Unset):
            types = []
            for types_item_data in self.types:
                types_item = types_item_data.value

                types.append(types_item)

        tags = self.tags
        not_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.not_names, Unset):
            not_names = self.not_names

        agent_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.agent_ids, Unset):
            agent_ids = self.agent_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sql_query is not UNSET:
            field_dict["sqlQuery"] = sql_query
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if limit is not UNSET:
            field_dict["limit"] = limit
        if stream_columns is not UNSET:
            field_dict["streamColumns"] = stream_columns
        if task_columns is not UNSET:
            field_dict["taskColumns"] = task_columns
        if aggregate_level is not UNSET:
            field_dict["aggregateLevel"] = aggregate_level
        if order_by_column is not UNSET:
            field_dict["orderByColumn"] = order_by_column
        if order_by_descending is not UNSET:
            field_dict["orderByDescending"] = order_by_descending
        if visible_columns is not UNSET:
            field_dict["visibleColumns"] = visible_columns
        if group_by_device is not UNSET:
            field_dict["groupByDevice"] = group_by_device
        if type is not UNSET:
            field_dict["type"] = type
        if unit is not UNSET:
            field_dict["unit"] = unit
        if device_ids is not UNSET:
            field_dict["deviceIds"] = device_ids
        if names is not UNSET:
            field_dict["names"] = names
        if types is not UNSET:
            field_dict["types"] = types
        if tags is not UNSET:
            field_dict["tags"] = tags
        if not_names is not UNSET:
            field_dict["notNames"] = not_names
        if agent_ids is not UNSET:
            field_dict["agentIds"] = agent_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.stream_column import StreamColumn
        from ..models.task_report_column import TaskReportColumn

        d = src_dict.copy()
        sql_query = d.pop("sqlQuery", UNSET)

        parameters = cast(List[str], d.pop("parameters", UNSET))

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = isoparse(_start)

        _end = d.pop("end", UNSET)
        end: Union[Unset, datetime.datetime]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = isoparse(_end)

        limit = d.pop("limit", UNSET)

        stream_columns = []
        _stream_columns = d.pop("streamColumns", UNSET)
        for stream_columns_item_data in _stream_columns or []:
            stream_columns_item = StreamColumn.from_dict(stream_columns_item_data)

            stream_columns.append(stream_columns_item)

        task_columns = []
        _task_columns = d.pop("taskColumns", UNSET)
        for task_columns_item_data in _task_columns or []:
            task_columns_item = TaskReportColumn.from_dict(task_columns_item_data)

            task_columns.append(task_columns_item)

        _aggregate_level = d.pop("aggregateLevel", UNSET)
        aggregate_level: Union[Unset, SqlQueryAggregateLevel]
        if isinstance(_aggregate_level, Unset):
            aggregate_level = UNSET
        else:
            aggregate_level = SqlQueryAggregateLevel(_aggregate_level)

        order_by_column = d.pop("orderByColumn", UNSET)

        order_by_descending = d.pop("orderByDescending", UNSET)

        visible_columns = cast(List[str], d.pop("visibleColumns", UNSET))

        group_by_device = d.pop("groupByDevice", UNSET)

        type = d.pop("type", UNSET)

        unit = d.pop("unit", UNSET)

        device_ids = cast(List[str], d.pop("deviceIds", UNSET))

        names = cast(List[str], d.pop("names", UNSET))

        types = []
        _types = d.pop("types", UNSET)
        for types_item_data in _types or []:
            types_item = SqlQueryTypesItem(types_item_data)

            types.append(types_item)

        tags = d.pop("tags", UNSET)

        not_names = cast(List[str], d.pop("notNames", UNSET))

        agent_ids = cast(List[str], d.pop("agentIds", UNSET))

        sql_query = cls(
            sql_query=sql_query,
            parameters=parameters,
            start=start,
            end=end,
            limit=limit,
            stream_columns=stream_columns,
            task_columns=task_columns,
            aggregate_level=aggregate_level,
            order_by_column=order_by_column,
            order_by_descending=order_by_descending,
            visible_columns=visible_columns,
            group_by_device=group_by_device,
            type=type,
            unit=unit,
            device_ids=device_ids,
            names=names,
            types=types,
            tags=tags,
            not_names=not_names,
            agent_ids=agent_ids,
        )

        sql_query.additional_properties = d
        return sql_query

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
