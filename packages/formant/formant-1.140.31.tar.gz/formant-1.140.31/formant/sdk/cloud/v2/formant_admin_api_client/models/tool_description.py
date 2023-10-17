from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ToolDescription")


@attr.s(auto_attribs=True)
class ToolDescription:
    """
    Attributes:
        name (str):
        prompt (str):
        description (str):
        model (str):
    """

    name: str
    prompt: str
    description: str
    model: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        prompt = self.prompt
        description = self.description
        model = self.model

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "prompt": prompt,
                "description": description,
                "model": model,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        prompt = d.pop("prompt")

        description = d.pop("description")

        model = d.pop("model")

        tool_description = cls(
            name=name,
            prompt=prompt,
            description=description,
            model=model,
        )

        tool_description.additional_properties = d
        return tool_description

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
