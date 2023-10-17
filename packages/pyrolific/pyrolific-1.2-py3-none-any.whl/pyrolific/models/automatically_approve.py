from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.automatically_approve_action import AutomaticallyApproveAction

T = TypeVar("T", bound="AutomaticallyApprove")


@attr.s(auto_attribs=True)
class AutomaticallyApprove:
    """
    Attributes:
        action (AutomaticallyApproveAction): The action to take
    """

    action: AutomaticallyApproveAction
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
        action = AutomaticallyApproveAction(d.pop("action"))

        automatically_approve = cls(
            action=action,
        )

        automatically_approve.additional_properties = d
        return automatically_approve

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
