from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ResponseAnswer")


@attr.s(auto_attribs=True)
class ResponseAnswer:
    """Responsible for defining a response to a question

    Attributes:
        answer_id (str): The answer ID.
        value (str): The answer option value selected. Example: Potato.
    """

    answer_id: str
    value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answer_id = self.answer_id
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer_id": answer_id,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        answer_id = d.pop("answer_id")

        value = d.pop("value")

        response_answer = cls(
            answer_id=answer_id,
            value=value,
        )

        response_answer.additional_properties = d
        return response_answer

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
