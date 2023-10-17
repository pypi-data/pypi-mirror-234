from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ParticipantIDs")


@attr.s(auto_attribs=True)
class ParticipantIDs:
    """
    Attributes:
        study_id (str):
        participant_ids (List[str]):
    """

    study_id: str
    participant_ids: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        study_id = self.study_id
        participant_ids = self.participant_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "study_id": study_id,
                "participant_ids": participant_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        study_id = d.pop("study_id")

        participant_ids = cast(List[str], d.pop("participant_ids"))

        participant_i_ds = cls(
            study_id=study_id,
            participant_ids=participant_ids,
        )

        participant_i_ds.additional_properties = d
        return participant_i_ds

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
