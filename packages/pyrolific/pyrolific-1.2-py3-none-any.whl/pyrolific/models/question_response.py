from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="QuestionResponse")


@attr.s(auto_attribs=True)
class QuestionResponse:
    """Responsible for defining an answer to a survey question

    Attributes:
        answers (List['ResponseAnswer']): The answers selected.
        question_id (str): The question ID.
        question_title (str): The title of the survey question.
    """

    answers: List["ResponseAnswer"]
    question_id: str
    question_title: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()

            answers.append(answers_item)

        question_id = self.question_id
        question_title = self.question_title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answers": answers,
                "question_id": question_id,
                "question_title": question_title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.response_answer import ResponseAnswer

        d = src_dict.copy()
        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = ResponseAnswer.from_dict(answers_item_data)

            answers.append(answers_item)

        question_id = d.pop("question_id")

        question_title = d.pop("question_title")

        question_response = cls(
            answers=answers,
            question_id=question_id,
            question_title=question_title,
        )

        question_response.additional_properties = d
        return question_response

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
