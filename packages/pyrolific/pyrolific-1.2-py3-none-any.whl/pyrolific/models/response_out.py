import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="ResponseOut")


@attr.s(auto_attribs=True)
class ResponseOut:
    """The model used to create a serialised representation a `Response`.

    Attributes:
        participant_id (str): The Prolific participant ID. Example: 62908f0b98a55b36ac68b992.
        submission_id (str): The Prolific submission ID. Example: 62908f0b98a55b36ac68b992.
        field_id (Union[Unset, str]):
        date_created (Union[Unset, datetime.datetime]): The date/time the response was created (UTC). Example:
            2022-05-27T08:43:12.
        date_modified (Union[Unset, datetime.datetime]): The date/time the response was modified (UTC). Example:
            2022-05-27T08:43:12.
        sections (Union[Unset, List['Section']]): An array of sections from the survey, otherwise `questions`.
        questions (Union[Unset, List['QuestionResponse']]): An array of questions from the survey, otherwise `sections`.
    """

    participant_id: str
    submission_id: str
    field_id: Union[Unset, str] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    date_modified: Union[Unset, datetime.datetime] = UNSET
    sections: Union[Unset, List["Section"]] = UNSET
    questions: Union[Unset, List["QuestionResponse"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        participant_id = self.participant_id
        submission_id = self.submission_id
        field_id = self.field_id
        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        date_modified: Union[Unset, str] = UNSET
        if not isinstance(self.date_modified, Unset):
            date_modified = self.date_modified.isoformat()

        sections: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sections, Unset):
            sections = []
            for sections_item_data in self.sections:
                sections_item = sections_item_data.to_dict()

                sections.append(sections_item)

        questions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.questions, Unset):
            questions = []
            for questions_item_data in self.questions:
                questions_item = questions_item_data.to_dict()

                questions.append(questions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "participant_id": participant_id,
                "submission_id": submission_id,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if date_modified is not UNSET:
            field_dict["date_modified"] = date_modified
        if sections is not UNSET:
            field_dict["sections"] = sections
        if questions is not UNSET:
            field_dict["questions"] = questions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.question_response import QuestionResponse
        from ..models.section import Section

        d = src_dict.copy()
        participant_id = d.pop("participant_id")

        submission_id = d.pop("submission_id")

        field_id = d.pop("_id", UNSET)

        _date_created = d.pop("date_created", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _date_modified = d.pop("date_modified", UNSET)
        date_modified: Union[Unset, datetime.datetime]
        if isinstance(_date_modified, Unset):
            date_modified = UNSET
        else:
            date_modified = isoparse(_date_modified)

        sections = []
        _sections = d.pop("sections", UNSET)
        for sections_item_data in _sections or []:
            sections_item = Section.from_dict(sections_item_data)

            sections.append(sections_item)

        questions = []
        _questions = d.pop("questions", UNSET)
        for questions_item_data in _questions or []:
            questions_item = QuestionResponse.from_dict(questions_item_data)

            questions.append(questions_item)

        response_out = cls(
            participant_id=participant_id,
            submission_id=submission_id,
            field_id=field_id,
            date_created=date_created,
            date_modified=date_modified,
            sections=sections,
            questions=questions,
        )

        response_out.additional_properties = d
        return response_out

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
