from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

if TYPE_CHECKING:
    from ..models.annotation import Annotation
    from ..models.command_delivery_event import CommandDeliveryEvent
    from ..models.comment import Comment
    from ..models.custom_event import CustomEvent
    from ..models.datapoint_event import DatapointEvent
    from ..models.device_offline_event import DeviceOfflineEvent
    from ..models.device_online_event import DeviceOnlineEvent
    from ..models.intervention_request import InterventionRequest
    from ..models.port_forwarding_session_record import PortForwardingSessionRecord
    from ..models.stateful_event import StatefulEvent
    from ..models.system_event import SystemEvent
    from ..models.task_summary import TaskSummary
    from ..models.teleop_session_record import TeleopSessionRecord


T = TypeVar("T", bound="EventListResponse")


@attr.s(auto_attribs=True)
class EventListResponse:
    """
    Attributes:
        items (List[Union['Annotation', 'CommandDeliveryEvent', 'Comment', 'CustomEvent', 'DatapointEvent',
            'DeviceOfflineEvent', 'DeviceOnlineEvent', 'InterventionRequest', 'PortForwardingSessionRecord',
            'StatefulEvent', 'SystemEvent', 'TaskSummary', 'TeleopSessionRecord']]):
    """

    items: List[
        Union[
            "Annotation",
            "CommandDeliveryEvent",
            "Comment",
            "CustomEvent",
            "DatapointEvent",
            "DeviceOfflineEvent",
            "DeviceOnlineEvent",
            "InterventionRequest",
            "PortForwardingSessionRecord",
            "StatefulEvent",
            "SystemEvent",
            "TaskSummary",
            "TeleopSessionRecord",
        ]
    ]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.annotation import Annotation
        from ..models.command_delivery_event import CommandDeliveryEvent
        from ..models.comment import Comment
        from ..models.custom_event import CustomEvent
        from ..models.datapoint_event import DatapointEvent
        from ..models.device_offline_event import DeviceOfflineEvent
        from ..models.device_online_event import DeviceOnlineEvent
        from ..models.intervention_request import InterventionRequest
        from ..models.port_forwarding_session_record import PortForwardingSessionRecord
        from ..models.system_event import SystemEvent
        from ..models.task_summary import TaskSummary
        from ..models.teleop_session_record import TeleopSessionRecord

        items = []
        for items_item_data in self.items:
            items_item: Dict[str, Any]

            if isinstance(items_item_data, DatapointEvent):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, DeviceOnlineEvent):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, DeviceOfflineEvent):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, InterventionRequest):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, TeleopSessionRecord):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, PortForwardingSessionRecord):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, CommandDeliveryEvent):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, CustomEvent):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, Comment):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, SystemEvent):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, Annotation):
                items_item = items_item_data.to_dict()

            elif isinstance(items_item_data, TaskSummary):
                items_item = items_item_data.to_dict()

            else:
                items_item = items_item_data.to_dict()

            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotation import Annotation
        from ..models.command_delivery_event import CommandDeliveryEvent
        from ..models.comment import Comment
        from ..models.custom_event import CustomEvent
        from ..models.datapoint_event import DatapointEvent
        from ..models.device_offline_event import DeviceOfflineEvent
        from ..models.device_online_event import DeviceOnlineEvent
        from ..models.intervention_request import InterventionRequest
        from ..models.port_forwarding_session_record import PortForwardingSessionRecord
        from ..models.stateful_event import StatefulEvent
        from ..models.system_event import SystemEvent
        from ..models.task_summary import TaskSummary
        from ..models.teleop_session_record import TeleopSessionRecord

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:

            def _parse_items_item(
                data: object,
            ) -> Union[
                "Annotation",
                "CommandDeliveryEvent",
                "Comment",
                "CustomEvent",
                "DatapointEvent",
                "DeviceOfflineEvent",
                "DeviceOnlineEvent",
                "InterventionRequest",
                "PortForwardingSessionRecord",
                "StatefulEvent",
                "SystemEvent",
                "TaskSummary",
                "TeleopSessionRecord",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_0 = DatapointEvent.from_dict(data)

                    return items_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_1 = DeviceOnlineEvent.from_dict(data)

                    return items_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_2 = DeviceOfflineEvent.from_dict(data)

                    return items_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_3 = InterventionRequest.from_dict(data)

                    return items_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_4 = TeleopSessionRecord.from_dict(data)

                    return items_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_5 = PortForwardingSessionRecord.from_dict(data)

                    return items_item_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_6 = CommandDeliveryEvent.from_dict(data)

                    return items_item_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_7 = CustomEvent.from_dict(data)

                    return items_item_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_8 = Comment.from_dict(data)

                    return items_item_type_8
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_9 = SystemEvent.from_dict(data)

                    return items_item_type_9
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_10 = Annotation.from_dict(data)

                    return items_item_type_10
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    items_item_type_11 = TaskSummary.from_dict(data)

                    return items_item_type_11
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                items_item_type_12 = StatefulEvent.from_dict(data)

                return items_item_type_12

            items_item = _parse_items_item(items_item_data)

            items.append(items_item)

        event_list_response = cls(
            items=items,
        )

        event_list_response.additional_properties = d
        return event_list_response

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
