from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.manually_review_action import ManuallyReviewAction

T = TypeVar("T", bound="ManuallyReview")


@attr.s(auto_attribs=True)
class ManuallyReview:
    """
    Attributes:
        action (ManuallyReviewAction): The action to take
    """

    action: ManuallyReviewAction
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = ManuallyReviewAction(d.pop("action"))

        manually_review = cls(
            action=action,
        )

        manually_review.additional_properties = d
        return manually_review

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
