import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.study_short_status import StudyShortStatus
from ..models.study_short_study_type import StudyShortStudyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudyShort")


@attr.s(auto_attribs=True)
class StudyShort:
    """
    Example:
        {'id': '60d9aadeb86739de712faee0', 'name': "Study about API's", 'status': 'UNPUBLISHED'}

    Attributes:
        id (str): Study id. It is created by Prolific.
        name (str): Public name or title of the study
        internal_name (Union[Unset, None, str]): Internal name of the study, not shown to participants
        status (Union[Unset, StudyShortStatus]): Status of the study.
        study_type (Union[Unset, StudyShortStudyType]): Deprecated. Type of study.
        total_available_places (Union[Unset, float]): How many participants are you looking to recruit
        places_taken (Union[Unset, float]): Places already taken, number of submission started excluding timed out and
            returned submissions
        number_of_submissions (Union[Unset, float]):
        reward (Union[Unset, float]): How much are you going to pay the participants in cents. We use the currency of
            your account
        total_cost (Union[Unset, float]): Total cost of the study including fees
        published_at (Union[Unset, None, datetime.datetime]): Date time when the study was published.
        publish_at (Union[Unset, None, datetime.datetime]): Date time when the study was scheduled to be published.
        date_created (Union[Unset, datetime.datetime]): Date time when the study was created
    """

    id: str
    name: str
    internal_name: Union[Unset, None, str] = UNSET
    status: Union[Unset, StudyShortStatus] = UNSET
    study_type: Union[Unset, StudyShortStudyType] = UNSET
    total_available_places: Union[Unset, float] = UNSET
    places_taken: Union[Unset, float] = UNSET
    number_of_submissions: Union[Unset, float] = UNSET
    reward: Union[Unset, float] = UNSET
    total_cost: Union[Unset, float] = UNSET
    published_at: Union[Unset, None, datetime.datetime] = UNSET
    publish_at: Union[Unset, None, datetime.datetime] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        internal_name = self.internal_name
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        study_type: Union[Unset, str] = UNSET
        if not isinstance(self.study_type, Unset):
            study_type = self.study_type.value

        total_available_places = self.total_available_places
        places_taken = self.places_taken
        number_of_submissions = self.number_of_submissions
        reward = self.reward
        total_cost = self.total_cost
        published_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.published_at, Unset):
            published_at = self.published_at.isoformat() if self.published_at else None

        publish_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.publish_at, Unset):
            publish_at = self.publish_at.isoformat() if self.publish_at else None

        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if internal_name is not UNSET:
            field_dict["internal_name"] = internal_name
        if status is not UNSET:
            field_dict["status"] = status
        if study_type is not UNSET:
            field_dict["study_type"] = study_type
        if total_available_places is not UNSET:
            field_dict["total_available_places"] = total_available_places
        if places_taken is not UNSET:
            field_dict["places_taken"] = places_taken
        if number_of_submissions is not UNSET:
            field_dict["number_of_submissions"] = number_of_submissions
        if reward is not UNSET:
            field_dict["reward"] = reward
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if published_at is not UNSET:
            field_dict["published_at"] = published_at
        if publish_at is not UNSET:
            field_dict["publish_at"] = publish_at
        if date_created is not UNSET:
            field_dict["date_created"] = date_created

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        internal_name = d.pop("internal_name", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, StudyShortStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = StudyShortStatus(_status)

        _study_type = d.pop("study_type", UNSET)
        study_type: Union[Unset, StudyShortStudyType]
        if isinstance(_study_type, Unset):
            study_type = UNSET
        else:
            study_type = StudyShortStudyType(_study_type)

        total_available_places = d.pop("total_available_places", UNSET)

        places_taken = d.pop("places_taken", UNSET)

        number_of_submissions = d.pop("number_of_submissions", UNSET)

        reward = d.pop("reward", UNSET)

        total_cost = d.pop("total_cost", UNSET)

        _published_at = d.pop("published_at", UNSET)
        published_at: Union[Unset, None, datetime.datetime]
        if _published_at is None:
            published_at = None
        elif isinstance(_published_at, Unset):
            published_at = UNSET
        else:
            published_at = isoparse(_published_at)

        _publish_at = d.pop("publish_at", UNSET)
        publish_at: Union[Unset, None, datetime.datetime]
        if _publish_at is None:
            publish_at = None
        elif isinstance(_publish_at, Unset):
            publish_at = UNSET
        else:
            publish_at = isoparse(_publish_at)

        _date_created = d.pop("date_created", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset):
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        study_short = cls(
            id=id,
            name=name,
            internal_name=internal_name,
            status=status,
            study_type=study_type,
            total_available_places=total_available_places,
            places_taken=places_taken,
            number_of_submissions=number_of_submissions,
            reward=reward,
            total_cost=total_cost,
            published_at=published_at,
            publish_at=publish_at,
            date_created=date_created,
        )

        study_short.additional_properties = d
        return study_short

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
