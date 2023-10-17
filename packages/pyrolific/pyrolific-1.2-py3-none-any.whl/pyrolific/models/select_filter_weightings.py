from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SelectFilterWeightings")


@attr.s(auto_attribs=True)
class SelectFilterWeightings:
    """Ratios to control the distribution of participants across the selected values.

    Integer percentages, floats, and exact quantities are valid inputs.

    """

    additional_properties: Dict[str, float] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        select_filter_weightings = cls()

        select_filter_weightings.additional_properties = d
        return select_filter_weightings

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> float:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: float) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
