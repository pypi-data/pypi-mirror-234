import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.partial_view_layout_type import PartialViewLayoutType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_ import Filter
    from ..models.partial_view_tags import PartialViewTags
    from ..models.view_configuration import ViewConfiguration


T = TypeVar("T", bound="PartialView")


@attr.s(auto_attribs=True)
class PartialView:
    """
    Attributes:
        organization_id (Union[Unset, str]):
        name (Union[Unset, str]):
        url (Union[Unset, None, str]):
        show_on_single_device (Union[Unset, bool]):
        show_on_multi_device (Union[Unset, bool]):
        show_on_teleop (Union[Unset, bool]):
        show_on_analytics (Union[Unset, bool]):
        show_timeline (Union[Unset, bool]):
        filter_ (Union[Unset, Filter]):
        layout (Union[Unset, Any]):
        layout_type (Union[Unset, None, PartialViewLayoutType]):
        configuration (Union[Unset, List['ViewConfiguration']]):
        smart_fleet_id (Union[Unset, None, str]):
        index (Union[Unset, int]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, PartialViewTags]):
    """

    organization_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    url: Union[Unset, None, str] = UNSET
    show_on_single_device: Union[Unset, bool] = UNSET
    show_on_multi_device: Union[Unset, bool] = UNSET
    show_on_teleop: Union[Unset, bool] = UNSET
    show_on_analytics: Union[Unset, bool] = UNSET
    show_timeline: Union[Unset, bool] = UNSET
    filter_: Union[Unset, "Filter"] = UNSET
    layout: Union[Unset, Any] = UNSET
    layout_type: Union[Unset, None, PartialViewLayoutType] = UNSET
    configuration: Union[Unset, List["ViewConfiguration"]] = UNSET
    smart_fleet_id: Union[Unset, None, str] = UNSET
    index: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "PartialViewTags"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        organization_id = self.organization_id
        name = self.name
        url = self.url
        show_on_single_device = self.show_on_single_device
        show_on_multi_device = self.show_on_multi_device
        show_on_teleop = self.show_on_teleop
        show_on_analytics = self.show_on_analytics
        show_timeline = self.show_timeline
        filter_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        layout = self.layout
        layout_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.layout_type, Unset):
            layout_type = self.layout_type.value if self.layout_type else None

        configuration: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = []
            for configuration_item_data in self.configuration:
                configuration_item = configuration_item_data.to_dict()

                configuration.append(configuration_item)

        smart_fleet_id = self.smart_fleet_id
        index = self.index
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
        if url is not UNSET:
            field_dict["url"] = url
        if show_on_single_device is not UNSET:
            field_dict["showOnSingleDevice"] = show_on_single_device
        if show_on_multi_device is not UNSET:
            field_dict["showOnMultiDevice"] = show_on_multi_device
        if show_on_teleop is not UNSET:
            field_dict["showOnTeleop"] = show_on_teleop
        if show_on_analytics is not UNSET:
            field_dict["showOnAnalytics"] = show_on_analytics
        if show_timeline is not UNSET:
            field_dict["showTimeline"] = show_timeline
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if layout is not UNSET:
            field_dict["layout"] = layout
        if layout_type is not UNSET:
            field_dict["layoutType"] = layout_type
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if smart_fleet_id is not UNSET:
            field_dict["smartFleetId"] = smart_fleet_id
        if index is not UNSET:
            field_dict["index"] = index
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
        from ..models.filter_ import Filter
        from ..models.partial_view_tags import PartialViewTags
        from ..models.view_configuration import ViewConfiguration

        d = src_dict.copy()
        organization_id = d.pop("organizationId", UNSET)

        name = d.pop("name", UNSET)

        url = d.pop("url", UNSET)

        show_on_single_device = d.pop("showOnSingleDevice", UNSET)

        show_on_multi_device = d.pop("showOnMultiDevice", UNSET)

        show_on_teleop = d.pop("showOnTeleop", UNSET)

        show_on_analytics = d.pop("showOnAnalytics", UNSET)

        show_timeline = d.pop("showTimeline", UNSET)

        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, Filter]
        if isinstance(_filter_, Unset):
            filter_ = UNSET
        else:
            filter_ = Filter.from_dict(_filter_)

        layout = d.pop("layout", UNSET)

        _layout_type = d.pop("layoutType", UNSET)
        layout_type: Union[Unset, None, PartialViewLayoutType]
        if _layout_type is None:
            layout_type = None
        elif isinstance(_layout_type, Unset):
            layout_type = UNSET
        else:
            layout_type = PartialViewLayoutType(_layout_type)

        configuration = []
        _configuration = d.pop("configuration", UNSET)
        for configuration_item_data in _configuration or []:
            configuration_item = ViewConfiguration.from_dict(configuration_item_data)

            configuration.append(configuration_item)

        smart_fleet_id = d.pop("smartFleetId", UNSET)

        index = d.pop("index", UNSET)

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
        tags: Union[Unset, PartialViewTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PartialViewTags.from_dict(_tags)

        partial_view = cls(
            organization_id=organization_id,
            name=name,
            url=url,
            show_on_single_device=show_on_single_device,
            show_on_multi_device=show_on_multi_device,
            show_on_teleop=show_on_teleop,
            show_on_analytics=show_on_analytics,
            show_timeline=show_timeline,
            filter_=filter_,
            layout=layout,
            layout_type=layout_type,
            configuration=configuration,
            smart_fleet_id=smart_fleet_id,
            index=index,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
        )

        partial_view.additional_properties = d
        return partial_view

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
