from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.request_return_action import RequestReturnAction

T = TypeVar("T", bound="RequestReturn")


@attr.s(auto_attribs=True)
class RequestReturn:
    """
    Attributes:
        action (RequestReturnAction): The action to take
        return_reason (str): The reason you would like to request a return Example: Failed an attention check.
    """

    action: RequestReturnAction
    return_reason: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action.value

        return_reason = self.return_reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "return_reason": return_reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = RequestReturnAction(d.pop("action"))

        return_reason = d.pop("return_reason")

        request_return = cls(
            action=action,
            return_reason=return_reason,
        )

        request_return.additional_properties = d
        return request_return

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
