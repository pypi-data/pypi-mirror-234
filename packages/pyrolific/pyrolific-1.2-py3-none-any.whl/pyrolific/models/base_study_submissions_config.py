from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseStudySubmissionsConfig")


@attr.s(auto_attribs=True)
class BaseStudySubmissionsConfig:
    """**BETA**: This is a beta feature and is currently only available to selected workspaces.
    It is being tested and evaluated for effectiveness and user experience before being released to all users.

    **Advanced**: This helps with faster data collection. Your survey system will need to handle providing a
    unique experience each time the participant takes the study.

    Configuration related to study submissions. The purpose of this field is to capture any configuration options that
    impact the submissions made by participants in a study.

        Attributes:
            max_submissions_per_participant (Union[Unset, None, int]): - **1** is the default Prolific experience. This
                means one submission, per participant, per study. If you do
                  not specify this field, the **default is 1**.
                - **1+** turns your study into a multi-submission study, meaning a participant can create many submissions per
                study.
                  As noted above, your survey system will need to handle providing a
                unique experience each time the participant takes the study.
                - **-1** will allow an indefinite number of submissions from a single participant, up to
                `total_available_places`. Default: 1.
            max_concurrent_submissions (Union[Unset, None, int]): - **-1** is the default value, meaning unlimited
                concurrent active/reserved submissions per study.
                - **1+** limits the number of concurrent active/reserved submissions a study can have at one time. Default: -1.
    """

    max_submissions_per_participant: Union[Unset, None, int] = 1
    max_concurrent_submissions: Union[Unset, None, int] = -1
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        max_submissions_per_participant = self.max_submissions_per_participant
        max_concurrent_submissions = self.max_concurrent_submissions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_submissions_per_participant is not UNSET:
            field_dict["max_submissions_per_participant"] = max_submissions_per_participant
        if max_concurrent_submissions is not UNSET:
            field_dict["max_concurrent_submissions"] = max_concurrent_submissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        max_submissions_per_participant = d.pop("max_submissions_per_participant", UNSET)

        max_concurrent_submissions = d.pop("max_concurrent_submissions", UNSET)

        base_study_submissions_config = cls(
            max_submissions_per_participant=max_submissions_per_participant,
            max_concurrent_submissions=max_concurrent_submissions,
        )

        base_study_submissions_config.additional_properties = d
        return base_study_submissions_config

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
