from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="ParticipantGroupFeederStudiesItem")


@attr.s(auto_attribs=True)
class ParticipantGroupFeederStudiesItem:
    """
    Attributes:
        id (Union[Unset, str]): The id of the study. Example: 5e9b9c9b0f9c9a0001b0b1f4.
        name (Union[Unset, str]): The name of the study. Example: Study 1.
        internal_name (Union[Unset, str]): The internal name of the study. Example: My Study.
        status (Union[Unset, str]): The current status of the study. Example: COMPLETED.
        feeder_completion_codes (Union[Unset, List['ParticipantGroupFeederStudiesItemFeederCompletionCodesItem']]): The
            completion codes which will modify the participants in this group.
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    internal_name: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    feeder_completion_codes: Union[Unset, List["ParticipantGroupFeederStudiesItemFeederCompletionCodesItem"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        internal_name = self.internal_name
        status = self.status
        feeder_completion_codes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.feeder_completion_codes, Unset):
            feeder_completion_codes = []
            for feeder_completion_codes_item_data in self.feeder_completion_codes:
                feeder_completion_codes_item = feeder_completion_codes_item_data.to_dict()

                feeder_completion_codes.append(feeder_completion_codes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if internal_name is not UNSET:
            field_dict["internal_name"] = internal_name
        if status is not UNSET:
            field_dict["status"] = status
        if feeder_completion_codes is not UNSET:
            field_dict["feeder_completion_codes"] = feeder_completion_codes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.participant_group_feeder_studies_item_feeder_completion_codes_item import (
            ParticipantGroupFeederStudiesItemFeederCompletionCodesItem,
        )

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        internal_name = d.pop("internal_name", UNSET)

        status = d.pop("status", UNSET)

        feeder_completion_codes = []
        _feeder_completion_codes = d.pop("feeder_completion_codes", UNSET)
        for feeder_completion_codes_item_data in _feeder_completion_codes or []:
            feeder_completion_codes_item = ParticipantGroupFeederStudiesItemFeederCompletionCodesItem.from_dict(
                feeder_completion_codes_item_data
            )

            feeder_completion_codes.append(feeder_completion_codes_item)

        participant_group_feeder_studies_item = cls(
            id=id,
            name=name,
            internal_name=internal_name,
            status=status,
            feeder_completion_codes=feeder_completion_codes,
        )

        participant_group_feeder_studies_item.additional_properties = d
        return participant_group_feeder_studies_item

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
