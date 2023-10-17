from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="SelectFilter")


@attr.s(auto_attribs=True)
class SelectFilter:
    r"""
    Attributes:
        filter_id (str): ID of the "select" type filter.
        selected_values (List[str]): This schema applies for filters of the `select` type, as defined in the [filter
            list response](\#tag/Filters/paths/~1api~1v1~1filters~1/get).

            Array of IDs matching the response IDs, from the `select` filter's `choices` (see response linked above).

            String format should match the `data_type` of the `select` filter's `choices` (see response linked above).
        weightings (Union[Unset, SelectFilterWeightings]): Ratios to control the distribution of participants across the
            selected values.

            Integer percentages, floats, and exact quantities are valid inputs.
    """

    filter_id: str
    selected_values: List[str]
    weightings: Union[Unset, "SelectFilterWeightings"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_id = self.filter_id
        selected_values = self.selected_values

        weightings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.weightings, Unset):
            weightings = self.weightings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filter_id": filter_id,
                "selected_values": selected_values,
            }
        )
        if weightings is not UNSET:
            field_dict["weightings"] = weightings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.select_filter_weightings import SelectFilterWeightings

        d = src_dict.copy()
        filter_id = d.pop("filter_id")

        selected_values = cast(List[str], d.pop("selected_values"))

        _weightings = d.pop("weightings", UNSET)
        weightings: Union[Unset, SelectFilterWeightings]
        if isinstance(_weightings, Unset):
            weightings = UNSET
        else:
            weightings = SelectFilterWeightings.from_dict(_weightings)

        select_filter = cls(
            filter_id=filter_id,
            selected_values=selected_values,
            weightings=weightings,
        )

        select_filter.additional_properties = d
        return select_filter

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
