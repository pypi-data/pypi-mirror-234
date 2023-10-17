from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SummaryAnswer")


@attr.s(auto_attribs=True)
class SummaryAnswer:
    """Responsible for housing the aggregation for a specific answer.

    Attributes:
        answer (str): The answer selected.
        answer_id (Union[Unset, str]): The answer ID.
        count (Union[Unset, int]): The count of how many times this answer was used in a response.
    """

    answer: str
    answer_id: Union[Unset, str] = UNSET
    count: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answer = self.answer
        answer_id = self.answer_id
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answer": answer,
            }
        )
        if answer_id is not UNSET:
            field_dict["answer_id"] = answer_id
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        answer = d.pop("answer")

        answer_id = d.pop("answer_id", UNSET)

        count = d.pop("count", UNSET)

        summary_answer = cls(
            answer=answer,
            answer_id=answer_id,
            count=count,
        )

        summary_answer.additional_properties = d
        return summary_answer

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
