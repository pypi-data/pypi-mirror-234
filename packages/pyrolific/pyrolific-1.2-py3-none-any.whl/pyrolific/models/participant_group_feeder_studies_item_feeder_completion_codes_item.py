from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.participant_group_feeder_studies_item_feeder_completion_codes_item_action import (
    ParticipantGroupFeederStudiesItemFeederCompletionCodesItemAction,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantGroupFeederStudiesItemFeederCompletionCodesItem")


@attr.s(auto_attribs=True)
class ParticipantGroupFeederStudiesItemFeederCompletionCodesItem:
    """The code within this study that interacts with the participant group.

    Attributes:
        code (Union[Unset, str]): The code that will modify the participants in this group. Example: AJVRH234.
        code_type (Union[Unset, str]): The label or code type given to this code within the context of the study.
            Example: COMPLETION_CODE.
        action (Union[Unset, ParticipantGroupFeederStudiesItemFeederCompletionCodesItemAction]): The action that will be
            taken when this code is used. Example: ADD_TO_PARTICIPANT_GROUP.
    """

    code: Union[Unset, str] = UNSET
    code_type: Union[Unset, str] = UNSET
    action: Union[Unset, ParticipantGroupFeederStudiesItemFeederCompletionCodesItemAction] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        code_type = self.code_type
        action: Union[Unset, str] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if code_type is not UNSET:
            field_dict["code_type"] = code_type
        if action is not UNSET:
            field_dict["action"] = action

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        code_type = d.pop("code_type", UNSET)

        _action = d.pop("action", UNSET)
        action: Union[Unset, ParticipantGroupFeederStudiesItemFeederCompletionCodesItemAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = ParticipantGroupFeederStudiesItemFeederCompletionCodesItemAction(_action)

        participant_group_feeder_studies_item_feeder_completion_codes_item = cls(
            code=code,
            code_type=code_type,
            action=action,
        )

        participant_group_feeder_studies_item_feeder_completion_codes_item.additional_properties = d
        return participant_group_feeder_studies_item_feeder_completion_codes_item

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
