from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="StudyCostResponse")


@attr.s(auto_attribs=True)
class StudyCostResponse:
    """
    Attributes:
        total_cost (float): Total cost of the study including VAT and fees in cents. We use your account VAT and Fee
            percentage. The amount is in your account's currency. Example: 56.
    """

    total_cost: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_cost = self.total_cost

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_cost": total_cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_cost = d.pop("total_cost")

        study_cost_response = cls(
            total_cost=total_cost,
        )

        study_cost_response.additional_properties = d
        return study_cost_response

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
