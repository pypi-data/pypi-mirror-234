from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="CompleteUploadRequest")


@attr.s(auto_attribs=True)
class CompleteUploadRequest:
    """
    Attributes:
        file_id (str):
        upload_id (str):
        e_tags (List[str]):
    """

    file_id: str
    upload_id: str
    e_tags: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_id = self.file_id
        upload_id = self.upload_id
        e_tags = self.e_tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fileId": file_id,
                "uploadId": upload_id,
                "eTags": e_tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_id = d.pop("fileId")

        upload_id = d.pop("uploadId")

        e_tags = cast(List[str], d.pop("eTags"))

        complete_upload_request = cls(
            file_id=file_id,
            upload_id=upload_id,
            e_tags=e_tags,
        )

        complete_upload_request.additional_properties = d
        return complete_upload_request

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
