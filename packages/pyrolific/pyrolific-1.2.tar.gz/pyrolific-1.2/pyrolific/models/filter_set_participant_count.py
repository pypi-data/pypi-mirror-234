from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterSetParticipantCount")


@attr.s(auto_attribs=True)
class FilterSetParticipantCount:
    """
    Attributes:
        eligible_participant_count (Union[Unset, int]): The number of participants who match the filter sets filters.
            Please note that if the number is
            lower than 25 the count will be obscured to prevent identification of participants.
    """

    eligible_participant_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eligible_participant_count = self.eligible_participant_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if eligible_participant_count is not UNSET:
            field_dict["eligible_participant_count"] = eligible_participant_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        eligible_participant_count = d.pop("eligible_participant_count", UNSET)

        filter_set_participant_count = cls(
            eligible_participant_count=eligible_participant_count,
        )

        filter_set_participant_count.additional_properties = d
        return filter_set_participant_count

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
