from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="CreateFilterSet")


@attr.s(auto_attribs=True)
class CreateFilterSet:
    """
    Example:
        [{'workspace_id': '644aaabfaf6bbc363b9d47c6', 'name': 'Ambidextrous teenagers', 'filters': [{'id': 'handedness',
            'selected_values': ['2']}, {'id': 'age', 'selected_range': {'lower': 18, 'upper': 19}}]}]

    Attributes:
        workspace_id (Union[Unset, str]): ID of the workspace where the filter set can be used.
        name (Union[Unset, str]): Name of the filter set.
        filters (Union[Unset, List[Union['RangeFilter', 'SelectFilter']]]): List of all filters contained in the filter
            set.
    """

    workspace_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    filters: Union[Unset, List[Union["RangeFilter", "SelectFilter"]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.select_filter import SelectFilter

        workspace_id = self.workspace_id
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
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
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
        workspace_id = d.pop("workspace_id", UNSET)

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

        create_filter_set = cls(
            workspace_id=workspace_id,
            name=name,
            filters=filters,
        )

        create_filter_set.additional_properties = d
        return create_filter_set

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
