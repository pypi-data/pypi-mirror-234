from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.base_study_completion_codes_item_code_type import BaseStudyCompletionCodesItemCodeType

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="BaseStudyCompletionCodesItem")


@attr.s(auto_attribs=True)
class BaseStudyCompletionCodesItem:
    """
    Attributes:
        code (str): The code the participant will either enter manually at the end of your study or be redirected as
            part of the return URL.
        code_type (BaseStudyCompletionCodesItemCodeType): A name for your code to make it easier to understand its
            intention. Either use one of the predefined options or any other free text.
        actions (List[Union['AddToParticipantGroup', 'AutomaticallyApprove', 'ManuallyReview',
            'RemoveFromParticipantGroup', 'RequestReturn']]): The actions that will be completed automatically when the
            submission is completed with this code.

            You can specify as many actions as you like. For a basic approach where all submissions are left for manual
            approval, set the `{"action": "MANUALLY_REVIEW"}` option only..
    """

    code: str
    code_type: BaseStudyCompletionCodesItemCodeType
    actions: List[
        Union[
            "AddToParticipantGroup",
            "AutomaticallyApprove",
            "ManuallyReview",
            "RemoveFromParticipantGroup",
            "RequestReturn",
        ]
    ]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.add_to_participant_group import AddToParticipantGroup
        from ..models.automatically_approve import AutomaticallyApprove
        from ..models.manually_review import ManuallyReview
        from ..models.remove_from_participant_group import RemoveFromParticipantGroup

        code = self.code
        code_type = self.code_type.value

        actions = []
        for actions_item_data in self.actions:
            actions_item: Dict[str, Any]

            if isinstance(actions_item_data, AutomaticallyApprove):
                actions_item = actions_item_data.to_dict()

            elif isinstance(actions_item_data, AddToParticipantGroup):
                actions_item = actions_item_data.to_dict()

            elif isinstance(actions_item_data, RemoveFromParticipantGroup):
                actions_item = actions_item_data.to_dict()

            elif isinstance(actions_item_data, ManuallyReview):
                actions_item = actions_item_data.to_dict()

            else:
                actions_item = actions_item_data.to_dict()

            actions.append(actions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "code_type": code_type,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.add_to_participant_group import AddToParticipantGroup
        from ..models.automatically_approve import AutomaticallyApprove
        from ..models.manually_review import ManuallyReview
        from ..models.remove_from_participant_group import RemoveFromParticipantGroup
        from ..models.request_return import RequestReturn

        d = src_dict.copy()
        code = d.pop("code")

        code_type = BaseStudyCompletionCodesItemCodeType(d.pop("code_type"))

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:

            def _parse_actions_item(
                data: object,
            ) -> Union[
                "AddToParticipantGroup",
                "AutomaticallyApprove",
                "ManuallyReview",
                "RemoveFromParticipantGroup",
                "RequestReturn",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_0 = AutomaticallyApprove.from_dict(data)

                    return actions_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_1 = AddToParticipantGroup.from_dict(data)

                    return actions_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_2 = RemoveFromParticipantGroup.from_dict(data)

                    return actions_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_3 = ManuallyReview.from_dict(data)

                    return actions_item_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                actions_item_type_4 = RequestReturn.from_dict(data)

                return actions_item_type_4

            actions_item = _parse_actions_item(actions_item_data)

            actions.append(actions_item)

        base_study_completion_codes_item = cls(
            code=code,
            code_type=code_type,
            actions=actions,
        )

        base_study_completion_codes_item.additional_properties = d
        return base_study_completion_codes_item

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
