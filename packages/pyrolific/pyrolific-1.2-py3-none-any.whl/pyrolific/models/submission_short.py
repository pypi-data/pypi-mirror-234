import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.submission_short_status import SubmissionShortStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmissionShort")


@attr.s(auto_attribs=True)
class SubmissionShort:
    """
    Example:
        {'id': '60d9aadeb86739de712faee0', 'participant_id': '60bf9310e8dec401be6e9615', 'started_at':
            datetime.datetime(2021, 5, 20, 11, 3, 0, 457000, tzinfo=datetime.timezone.utc), 'status': 'ACTIVE',
            'study_code': 'ABC123'}

    Attributes:
        id (str): Submission id.
        participant_id (str): Participant id.
        status (SubmissionShortStatus): Status of the submission.
        started_at (datetime.datetime): Date started
        has_siblings (bool): Whether or not the submission has sibling submissions (sharing the same study).
        completed_at (Union[Unset, None, datetime.datetime]): Date completed
        study_code (Union[Unset, None, str]): The completion code used by the participant to complete the study.
    """

    id: str
    participant_id: str
    status: SubmissionShortStatus
    started_at: datetime.datetime
    has_siblings: bool
    completed_at: Union[Unset, None, datetime.datetime] = UNSET
    study_code: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        participant_id = self.participant_id
        status = self.status.value

        started_at = self.started_at.isoformat()

        has_siblings = self.has_siblings
        completed_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat() if self.completed_at else None

        study_code = self.study_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "participant_id": participant_id,
                "status": status,
                "started_at": started_at,
                "has_siblings": has_siblings,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if study_code is not UNSET:
            field_dict["study_code"] = study_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        participant_id = d.pop("participant_id")

        status = SubmissionShortStatus(d.pop("status"))

        started_at = isoparse(d.pop("started_at"))

        has_siblings = d.pop("has_siblings")

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: Union[Unset, None, datetime.datetime]
        if _completed_at is None:
            completed_at = None
        elif isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        study_code = d.pop("study_code", UNSET)

        submission_short = cls(
            id=id,
            participant_id=participant_id,
            status=status,
            started_at=started_at,
            has_siblings=has_siblings,
            completed_at=completed_at,
            study_code=study_code,
        )

        submission_short.additional_properties = d
        return submission_short

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
