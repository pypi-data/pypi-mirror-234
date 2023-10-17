from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="FilterList")


@attr.s(auto_attribs=True)
class FilterList:
    """
    Attributes:
        results (Union[Unset, List[Union['RangeFilterListDetailedResponse', 'RangeFilterListResponse',
            'SelectFilterListDetailedResponse', 'SelectFilterListResponse']]]):
        field_links (Union[Unset, FilterListLinks]):
        meta (Union[Unset, FilterListMeta]):
    """

    results: Union[
        Unset,
        List[
            Union[
                "RangeFilterListDetailedResponse",
                "RangeFilterListResponse",
                "SelectFilterListDetailedResponse",
                "SelectFilterListResponse",
            ]
        ],
    ] = UNSET
    field_links: Union[Unset, "FilterListLinks"] = UNSET
    meta: Union[Unset, "FilterListMeta"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.range_filter_list_response import RangeFilterListResponse
        from ..models.select_filter_list_detailed_response import SelectFilterListDetailedResponse
        from ..models.select_filter_list_response import SelectFilterListResponse

        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item: Dict[str, Any]

                if isinstance(results_item_data, SelectFilterListResponse):
                    results_item = results_item_data.to_dict()

                elif isinstance(results_item_data, SelectFilterListDetailedResponse):
                    results_item = results_item_data.to_dict()

                elif isinstance(results_item_data, RangeFilterListResponse):
                    results_item = results_item_data.to_dict()

                else:
                    results_item = results_item_data.to_dict()

                results.append(results_item)

        field_links: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = self.field_links.to_dict()

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if results is not UNSET:
            field_dict["results"] = results
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.filter_list_links import FilterListLinks
        from ..models.filter_list_meta import FilterListMeta
        from ..models.range_filter_list_detailed_response import RangeFilterListDetailedResponse
        from ..models.range_filter_list_response import RangeFilterListResponse
        from ..models.select_filter_list_detailed_response import SelectFilterListDetailedResponse
        from ..models.select_filter_list_response import SelectFilterListResponse

        d = src_dict.copy()
        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:

            def _parse_results_item(
                data: object,
            ) -> Union[
                "RangeFilterListDetailedResponse",
                "RangeFilterListResponse",
                "SelectFilterListDetailedResponse",
                "SelectFilterListResponse",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    results_item_type_0 = SelectFilterListResponse.from_dict(data)

                    return results_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    results_item_type_1 = SelectFilterListDetailedResponse.from_dict(data)

                    return results_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    results_item_type_2 = RangeFilterListResponse.from_dict(data)

                    return results_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                results_item_type_3 = RangeFilterListDetailedResponse.from_dict(data)

                return results_item_type_3

            results_item = _parse_results_item(results_item_data)

            results.append(results_item)

        _field_links = d.pop("_links", UNSET)
        field_links: Union[Unset, FilterListLinks]
        if isinstance(_field_links, Unset):
            field_links = UNSET
        else:
            field_links = FilterListLinks.from_dict(_field_links)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, FilterListMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = FilterListMeta.from_dict(_meta)

        filter_list = cls(
            results=results,
            field_links=field_links,
            meta=meta,
        )

        filter_list.additional_properties = d
        return filter_list

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
