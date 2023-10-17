from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantGroupMembership")


@attr.s(auto_attribs=True)
class ParticipantGroupMembership:
    """
    Attributes:
        participant_id (Union[Unset, str]): The id of the participant Example: 5e9b9c9b0f9c9a0001b0b1f5.
        datetime_created (Union[Unset, str]): The date and time the participant was added to the Participant Group
            Example: 2020-04-20T12:00:00Z.
    """

    participant_id: Union[Unset, str] = UNSET
    datetime_created: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        participant_id = self.participant_id
        datetime_created = self.datetime_created

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if participant_id is not UNSET:
            field_dict["participant_id"] = participant_id
        if datetime_created is not UNSET:
            field_dict["datetime_created"] = datetime_created

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        participant_id = d.pop("participant_id", UNSET)

        datetime_created = d.pop("datetime_created", UNSET)

        participant_group_membership = cls(
            participant_id=participant_id,
            datetime_created=datetime_created,
        )

        participant_group_membership.additional_properties = d
        return participant_group_membership

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
