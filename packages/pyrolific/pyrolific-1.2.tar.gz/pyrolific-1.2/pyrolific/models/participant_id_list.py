from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantIDList")


@attr.s(auto_attribs=True)
class ParticipantIDList:
    """
    Attributes:
        participant_ids (Union[Unset, List[str]]):
    """

    participant_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        participant_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.participant_ids, Unset):
            participant_ids = self.participant_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if participant_ids is not UNSET:
            field_dict["participant_ids"] = participant_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        participant_ids = cast(List[str], d.pop("participant_ids", UNSET))

        participant_id_list = cls(
            participant_ids=participant_ids,
        )

        participant_id_list.additional_properties = d
        return participant_id_list

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
