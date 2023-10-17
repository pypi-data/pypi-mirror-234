from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="SummaryQuestion")


@attr.s(auto_attribs=True)
class SummaryQuestion:
    """Responsible for housing the questions we want to aggregate for the summary.

    Attributes:
        question (str): The title of the question.
        question_id (Union[Unset, str]): The question ID.
        total_answers (Union[Unset, int]): The total number of answered responses for a given question.
        answers (Union[Unset, List['SummaryAnswer']]): A list of aggregated answer information.
    """

    question: str
    question_id: Union[Unset, str] = UNSET
    total_answers: Union[Unset, int] = 0
    answers: Union[Unset, List["SummaryAnswer"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        question = self.question
        question_id = self.question_id
        total_answers = self.total_answers
        answers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.answers, Unset):
            answers = []
            for answers_item_data in self.answers:
                answers_item = answers_item_data.to_dict()

                answers.append(answers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "question": question,
            }
        )
        if question_id is not UNSET:
            field_dict["question_id"] = question_id
        if total_answers is not UNSET:
            field_dict["total_answers"] = total_answers
        if answers is not UNSET:
            field_dict["answers"] = answers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.summary_answer import SummaryAnswer

        d = src_dict.copy()
        question = d.pop("question")

        question_id = d.pop("question_id", UNSET)

        total_answers = d.pop("total_answers", UNSET)

        answers = []
        _answers = d.pop("answers", UNSET)
        for answers_item_data in _answers or []:
            answers_item = SummaryAnswer.from_dict(answers_item_data)

            answers.append(answers_item)

        summary_question = cls(
            question=question,
            question_id=question_id,
            total_answers=total_answers,
            answers=answers,
        )

        summary_question.additional_properties = d
        return summary_question

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
