from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="RequestSubmissionReturnJsonBody")


@attr.s(auto_attribs=True)
class RequestSubmissionReturnJsonBody:
    """
    Example:
        {'request_return_reasons': ['Withdrew consent.', 'Did not finish study.']}

    Attributes:
        request_return_reasons (List[str]):
    """

    request_return_reasons: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        request_return_reasons = self.request_return_reasons

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request_return_reasons": request_return_reasons,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        request_return_reasons = cast(List[str], d.pop("request_return_reasons"))

        request_submission_return_json_body = cls(
            request_return_reasons=request_return_reasons,
        )

        request_submission_return_json_body.additional_properties = d
        return request_submission_return_json_body

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
