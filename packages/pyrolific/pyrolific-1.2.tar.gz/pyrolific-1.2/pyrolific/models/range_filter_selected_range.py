from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RangeFilterSelectedRange")


@attr.s(auto_attribs=True)
class RangeFilterSelectedRange:
    r"""This schema applies for filters of the `range` type, as defined in the [filter list
    response](\#tag/Filters/paths/~1api~1v1~1filters~1/get).

    A dictionary with two possible objects, 'lower' and 'upper'. At least one must be present and a non-null value.

    The expected data type for these values is defined by the `range` filter's `data_type` (see response linked above).

    If the data_type is a date, string format should be a parseable ISO8601 date string. Date values should be provided
    as a string in ISO 8601 format.

    Leaving a value as null will result in that bound being set to the lowest or highest possible value, depending on
    whether it is the upper or lower bound.

        Attributes:
            lower (Union[Unset, int, str]): Your selected lower bound for the range.
            upper (Union[Unset, int, str]): Your selected upper bound for the range.
    """

    lower: Union[Unset, int, str] = UNSET
    upper: Union[Unset, int, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lower: Union[Unset, int, str]
        if isinstance(self.lower, Unset):
            lower = UNSET

        else:
            lower = self.lower

        upper: Union[Unset, int, str]
        if isinstance(self.upper, Unset):
            upper = UNSET

        else:
            upper = self.upper

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lower is not UNSET:
            field_dict["lower"] = lower
        if upper is not UNSET:
            field_dict["upper"] = upper

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_lower(data: object) -> Union[Unset, int, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, int, str], data)

        lower = _parse_lower(d.pop("lower", UNSET))

        def _parse_upper(data: object) -> Union[Unset, int, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, int, str], data)

        upper = _parse_upper(d.pop("upper", UNSET))

        range_filter_selected_range = cls(
            lower=lower,
            upper=upper,
        )

        range_filter_selected_range.additional_properties = d
        return range_filter_selected_range

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
