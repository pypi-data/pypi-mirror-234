from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="UpdateFilterSet")


@attr.s(auto_attribs=True)
class UpdateFilterSet:
    """
    Example:
        [{'name': 'Left-handed 30-somethings', 'filters': [{'id': 'handedness', 'selected_values': ['1']}, {'id': 'age',
            'selected_range': {'lower': 30, 'upper': 39}}]}]

    Attributes:
        name (Union[Unset, str]): Name of the filter set.
        filters (Union[Unset, List[Union['RangeFilter', 'SelectFilter']]]): List of all filters contained in the filter
            set.
    """

    name: Union[Unset, str] = UNSET
    filters: Union[Unset, List[Union["RangeFilter", "SelectFilter"]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.select_filter import SelectFilter

        name = self.name
        filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: Dict[str, Any]

                if isinstance(filters_item_data, SelectFilter):
                    filters_item = filters_item_data.to_dict()

                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.range_filter import RangeFilter
        from ..models.select_filter import SelectFilter

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(data: object) -> Union["RangeFilter", "SelectFilter"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = SelectFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_1 = RangeFilter.from_dict(data)

                return filters_item_type_1

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        update_filter_set = cls(
            name=name,
            filters=filters,
        )

        update_filter_set.additional_properties = d
        return update_filter_set

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
