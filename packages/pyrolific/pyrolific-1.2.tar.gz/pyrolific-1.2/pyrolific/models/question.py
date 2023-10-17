from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.question_type import QuestionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="Question")


@attr.s(auto_attribs=True)
class Question:
    """Responsible for defining a question within a survey.

    Attributes:
        answers (List['AnswerOption']): An array of answer options for a question.
        title (str): The question title. Example: What is your favourite root vegetable?.
        type (QuestionType): Responsible for articulating the question type. At the moment we have:

            - single answer
            - multiple answer

            Args:
                str (_type_): The type of question.
                Enum (_type_): The class to define an enum.
        id (Union[Unset, str]):
    """

    answers: List["AnswerOption"]
    title: str
    type: QuestionType
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()

            answers.append(answers_item)

        title = self.title
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "answers": answers,
                "title": title,
                "type": type,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.answer_option import AnswerOption

        d = src_dict.copy()
        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = AnswerOption.from_dict(answers_item_data)

            answers.append(answers_item)

        title = d.pop("title")

        type = QuestionType(d.pop("type"))

        id = d.pop("id", UNSET)

        question = cls(
            answers=answers,
            title=title,
            type=type,
            id=id,
        )

        question.additional_properties = d
        return question

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
