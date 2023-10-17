from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateParticipantGroupJsonBody")


@attr.s(auto_attribs=True)
class CreateParticipantGroupJsonBody:
    """
    Attributes:
        project_id (str): The id of the project to create the participant group in Example: 5e9b9c9b0f9c9a0001b0b1f4.
        name (str): The name of the participant group Example: Group 1.
        participant_ids (Union[Unset, List[str]]): The ids of participants to be initially added to the group Example:
            ['5e9b9c9b0f9c9a0001b0b1f4', '5e9b9c9b0f9c9a0001b0b1f5', '5e9b9c9b0f9c9a0001b0b1f6'].
    """

    project_id: str
    name: str
    participant_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        name = self.name
        participant_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.participant_ids, Unset):
            participant_ids = self.participant_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "name": name,
            }
        )
        if participant_ids is not UNSET:
            field_dict["participant_ids"] = participant_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        name = d.pop("name")

        participant_ids = cast(List[str], d.pop("participant_ids", UNSET))

        create_participant_group_json_body = cls(
            project_id=project_id,
            name=name,
            participant_ids=participant_ids,
        )

        create_participant_group_json_body.additional_properties = d
        return create_participant_group_json_body

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
