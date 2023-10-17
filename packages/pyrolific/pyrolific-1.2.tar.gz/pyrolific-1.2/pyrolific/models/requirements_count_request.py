from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="RequirementsCountRequest")


@attr.s(auto_attribs=True)
class RequirementsCountRequest:
    """
    Attributes:
        filters (List[Union['RangeFilter', 'SelectFilter']]): List of filters to apply to the count. This parameter uses
            the new, simplified
            filters schema for interacting with eligibility.
        workspace_id (str): The ID of the workspace you will be creating a study in.

            Due to US tax laws, non US residents may not participate in studies created by US researchers.
            For this reason, we use the country specified in the workspace to determine eligibility.

            If you do not specify a workspace ID, we will use the current workspace ID of the user making the request.
            Your eligibility count may not be accurate if you do not specify a workspace ID.
    """

    filters: List[Union["RangeFilter", "SelectFilter"]]
    workspace_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.select_filter import SelectFilter

        filters = []
        for filters_item_data in self.filters:
            filters_item: Dict[str, Any]

            if isinstance(filters_item_data, SelectFilter):
                filters_item = filters_item_data.to_dict()

            else:
                filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filters": filters,
                "workspace_id": workspace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.range_filter import RangeFilter
        from ..models.select_filter import SelectFilter

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:

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

        workspace_id = d.pop("workspace_id")

        requirements_count_request = cls(
            filters=filters,
            workspace_id=workspace_id,
        )

        requirements_count_request.additional_properties = d
        return requirements_count_request

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
