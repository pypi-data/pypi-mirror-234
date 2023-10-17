from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.submission_transition_action import SubmissionTransitionAction
from ..models.submission_transition_rejection_category import SubmissionTransitionRejectionCategory
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmissionTransition")


@attr.s(auto_attribs=True)
class SubmissionTransition:
    """
    Attributes:
        action (SubmissionTransitionAction): Action to execute. Example: APPROVE.
        message (Union[Unset, str]): Required if action is 'REJECT'. Message sent to the participant
            explaining the reason for the rejection.
            It must be at least 100 chars long. Example: Good explanation of the situation..
        rejection_category (Union[Unset, SubmissionTransitionRejectionCategory]): Required if action is 'REJECT', it
            sums as the category of
            the rejection. Example: LOW_EFFORT.
    """

    action: SubmissionTransitionAction
    message: Union[Unset, str] = UNSET
    rejection_category: Union[Unset, SubmissionTransitionRejectionCategory] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action.value

        message = self.message
        rejection_category: Union[Unset, str] = UNSET
        if not isinstance(self.rejection_category, Unset):
            rejection_category = self.rejection_category.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if rejection_category is not UNSET:
            field_dict["rejection_category"] = rejection_category

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = SubmissionTransitionAction(d.pop("action"))

        message = d.pop("message", UNSET)

        _rejection_category = d.pop("rejection_category", UNSET)
        rejection_category: Union[Unset, SubmissionTransitionRejectionCategory]
        if isinstance(_rejection_category, Unset):
            rejection_category = UNSET
        else:
            rejection_category = SubmissionTransitionRejectionCategory(_rejection_category)

        submission_transition = cls(
            action=action,
            message=message,
            rejection_category=rejection_category,
        )

        submission_transition.additional_properties = d
        return submission_transition

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
