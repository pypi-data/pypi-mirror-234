import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.partial_annotation_stream_type import PartialAnnotationStreamType
from ..models.partial_annotation_type import PartialAnnotationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_annotation_metadata import PartialAnnotationMetadata
    from ..models.partial_annotation_tags import PartialAnnotationTags


T = TypeVar("T", bound="PartialAnnotation")


@attr.s(auto_attribs=True)
class PartialAnnotation:
    """
    Attributes:
        type (Union[Unset, PartialAnnotationType]):
        edited_at (Union[Unset, None, datetime.datetime]):
        user_id (Union[Unset, str]):
        annotation_template_id (Union[Unset, None, str]):
        tagged_users (Union[Unset, Any]):
        published_to (Union[Unset, Any]):
        note (Union[Unset, None, str]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, PartialAnnotationTags]):
        organization_id (Union[Unset, str]):
        time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, None, datetime.datetime]):
        parent_id (Union[Unset, str]):
        metadata (Union[Unset, PartialAnnotationMetadata]):
        message (Union[Unset, str]):
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]):
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, PartialAnnotationStreamType]):
        event_trigger_id (Union[Unset, None, str]):
        notification_enabled (Union[Unset, bool]):
    """

    type: Union[Unset, PartialAnnotationType] = UNSET
    edited_at: Union[Unset, None, datetime.datetime] = UNSET
    user_id: Union[Unset, str] = UNSET
    annotation_template_id: Union[Unset, None, str] = UNSET
    tagged_users: Union[Unset, Any] = UNSET
    published_to: Union[Unset, Any] = UNSET
    note: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "PartialAnnotationTags"] = UNSET
    organization_id: Union[Unset, str] = UNSET
    time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    parent_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "PartialAnnotationMetadata"] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, PartialAnnotationStreamType] = UNSET
    event_trigger_id: Union[Unset, None, str] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        edited_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat() if self.edited_at else None

        user_id = self.user_id
        annotation_template_id = self.annotation_template_id
        tagged_users = self.tagged_users
        published_to = self.published_to
        note = self.note
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

        organization_id = self.organization_id
        time: Union[Unset, str] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        end_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat() if self.end_time else None

        parent_id = self.parent_id
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        message = self.message
        viewed = self.viewed
        device_id = self.device_id
        stream_name = self.stream_name
        stream_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.stream_type, Unset):
            stream_type = self.stream_type.value if self.stream_type else None

        event_trigger_id = self.event_trigger_id
        notification_enabled = self.notification_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if edited_at is not UNSET:
            field_dict["editedAt"] = edited_at
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if annotation_template_id is not UNSET:
            field_dict["annotationTemplateId"] = annotation_template_id
        if tagged_users is not UNSET:
            field_dict["taggedUsers"] = tagged_users
        if published_to is not UNSET:
            field_dict["publishedTo"] = published_to
        if note is not UNSET:
            field_dict["note"] = note
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if time is not UNSET:
            field_dict["time"] = time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if message is not UNSET:
            field_dict["message"] = message
        if viewed is not UNSET:
            field_dict["viewed"] = viewed
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if stream_name is not UNSET:
            field_dict["streamName"] = stream_name
        if stream_type is not UNSET:
            field_dict["streamType"] = stream_type
        if event_trigger_id is not UNSET:
            field_dict["eventTriggerId"] = event_trigger_id
        if notification_enabled is not UNSET:
            field_dict["notificationEnabled"] = notification_enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.partial_annotation_metadata import PartialAnnotationMetadata
        from ..models.partial_annotation_tags import PartialAnnotationTags

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, PartialAnnotationType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PartialAnnotationType(_type)

        _edited_at = d.pop("editedAt", UNSET)
        edited_at: Union[Unset, None, datetime.datetime]
        if _edited_at is None:
            edited_at = None
        elif isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

        user_id = d.pop("userId", UNSET)

        annotation_template_id = d.pop("annotationTemplateId", UNSET)

        tagged_users = d.pop("taggedUsers", UNSET)

        published_to = d.pop("publishedTo", UNSET)

        note = d.pop("note", UNSET)

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
        tags: Union[Unset, PartialAnnotationTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PartialAnnotationTags.from_dict(_tags)

        organization_id = d.pop("organizationId", UNSET)

        _time = d.pop("time", UNSET)
        time: Union[Unset, datetime.datetime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, None, datetime.datetime]
        if _end_time is None:
            end_time = None
        elif isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        parent_id = d.pop("parentId", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, PartialAnnotationMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = PartialAnnotationMetadata.from_dict(_metadata)

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, PartialAnnotationStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = PartialAnnotationStreamType(_stream_type)

        event_trigger_id = d.pop("eventTriggerId", UNSET)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        partial_annotation = cls(
            type=type,
            edited_at=edited_at,
            user_id=user_id,
            annotation_template_id=annotation_template_id,
            tagged_users=tagged_users,
            published_to=published_to,
            note=note,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
            organization_id=organization_id,
            time=time,
            end_time=end_time,
            parent_id=parent_id,
            metadata=metadata,
            message=message,
            viewed=viewed,
            device_id=device_id,
            stream_name=stream_name,
            stream_type=stream_type,
            event_trigger_id=event_trigger_id,
            notification_enabled=notification_enabled,
        )

        partial_annotation.additional_properties = d
        return partial_annotation

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
