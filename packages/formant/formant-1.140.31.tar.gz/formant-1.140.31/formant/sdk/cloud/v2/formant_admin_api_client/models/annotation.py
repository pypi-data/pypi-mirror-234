import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.annotation_stream_type import AnnotationStreamType
from ..models.annotation_type import AnnotationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_metadata import AnnotationMetadata
    from ..models.annotation_tags import AnnotationTags


T = TypeVar("T", bound="Annotation")


@attr.s(auto_attribs=True)
class Annotation:
    """
    Attributes:
        user_id (str):
        time (datetime.datetime):
        type (Union[Unset, AnnotationType]):
        edited_at (Union[Unset, None, datetime.datetime]):
        annotation_template_id (Union[Unset, None, str]):
        tagged_users (Union[Unset, Any]):
        published_to (Union[Unset, Any]):
        note (Union[Unset, None, str]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, AnnotationTags]):
        organization_id (Union[Unset, str]):
        end_time (Union[Unset, None, datetime.datetime]):
        parent_id (Union[Unset, str]):
        metadata (Union[Unset, AnnotationMetadata]):
        message (Union[Unset, str]):
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]):
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, AnnotationStreamType]):
        event_trigger_id (Union[Unset, None, str]):
        notification_enabled (Union[Unset, bool]):
    """

    user_id: str
    time: datetime.datetime
    type: Union[Unset, AnnotationType] = UNSET
    edited_at: Union[Unset, None, datetime.datetime] = UNSET
    annotation_template_id: Union[Unset, None, str] = UNSET
    tagged_users: Union[Unset, Any] = UNSET
    published_to: Union[Unset, Any] = UNSET
    note: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "AnnotationTags"] = UNSET
    organization_id: Union[Unset, str] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    parent_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "AnnotationMetadata"] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, AnnotationStreamType] = UNSET
    event_trigger_id: Union[Unset, None, str] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id
        time = self.time.isoformat()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        edited_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.edited_at, Unset):
            edited_at = self.edited_at.isoformat() if self.edited_at else None

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
        field_dict.update(
            {
                "userId": user_id,
                "time": time,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if edited_at is not UNSET:
            field_dict["editedAt"] = edited_at
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
        from ..models.annotation_metadata import AnnotationMetadata
        from ..models.annotation_tags import AnnotationTags

        d = src_dict.copy()
        user_id = d.pop("userId")

        time = isoparse(d.pop("time"))

        _type = d.pop("type", UNSET)
        type: Union[Unset, AnnotationType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AnnotationType(_type)

        _edited_at = d.pop("editedAt", UNSET)
        edited_at: Union[Unset, None, datetime.datetime]
        if _edited_at is None:
            edited_at = None
        elif isinstance(_edited_at, Unset):
            edited_at = UNSET
        else:
            edited_at = isoparse(_edited_at)

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
        tags: Union[Unset, AnnotationTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = AnnotationTags.from_dict(_tags)

        organization_id = d.pop("organizationId", UNSET)

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
        metadata: Union[Unset, AnnotationMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = AnnotationMetadata.from_dict(_metadata)

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, AnnotationStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = AnnotationStreamType(_stream_type)

        event_trigger_id = d.pop("eventTriggerId", UNSET)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        annotation = cls(
            user_id=user_id,
            time=time,
            type=type,
            edited_at=edited_at,
            annotation_template_id=annotation_template_id,
            tagged_users=tagged_users,
            published_to=published_to,
            note=note,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
            organization_id=organization_id,
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

        annotation.additional_properties = d
        return annotation

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
