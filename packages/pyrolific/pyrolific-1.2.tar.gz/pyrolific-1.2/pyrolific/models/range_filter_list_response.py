from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.filter_list_attributes_type import FilterListAttributesType
from ..models.range_filter_list_attributes_data_type import RangeFilterListAttributesDataType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RangeFilterListResponse")


@attr.s(auto_attribs=True)
class RangeFilterListResponse:
    """
    Attributes:
        filter_id (Union[Unset, str]): The ID of the filter, based on a slugified version of the title at the time the
            filter was created.
        title (Union[Unset, str]): The title of the filter.
        description (Union[Unset, str]): A description of the filter.
        type (Union[Unset, FilterListAttributesType]): The filter type.
        question (Union[Unset, str]): The question asked of participants to generate this filter.
        min_ (Union[Unset, int, str]): The minimum valid value of the range.
        max_ (Union[Unset, int, str]): The maximum valid value of the range.
        data_type (Union[Unset, RangeFilterListAttributesDataType]): The data type of the range. If the data type is
            integer, the lower and upper values must be integers.
            If the data type is date, the lower and upper values must be ISO8601 dates.
    """

    filter_id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type: Union[Unset, FilterListAttributesType] = UNSET
    question: Union[Unset, str] = UNSET
    min_: Union[Unset, int, str] = UNSET
    max_: Union[Unset, int, str] = UNSET
    data_type: Union[Unset, RangeFilterListAttributesDataType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_id = self.filter_id
        title = self.title
        description = self.description
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        question = self.question
        min_: Union[Unset, int, str]
        if isinstance(self.min_, Unset):
            min_ = UNSET

        else:
            min_ = self.min_

        max_: Union[Unset, int, str]
        if isinstance(self.max_, Unset):
            max_ = UNSET

        else:
            max_ = self.max_

        data_type: Union[Unset, str] = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = self.data_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_id is not UNSET:
            field_dict["filter_id"] = filter_id
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if question is not UNSET:
            field_dict["question"] = question
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if data_type is not UNSET:
            field_dict["data_type"] = data_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_id = d.pop("filter_id", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, FilterListAttributesType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = FilterListAttributesType(_type)

        question = d.pop("question", UNSET)

        def _parse_min_(data: object) -> Union[Unset, int, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, int, str], data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> Union[Unset, int, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, int, str], data)

        max_ = _parse_max_(d.pop("max", UNSET))

        _data_type = d.pop("data_type", UNSET)
        data_type: Union[Unset, RangeFilterListAttributesDataType]
        if isinstance(_data_type, Unset):
            data_type = UNSET
        else:
            data_type = RangeFilterListAttributesDataType(_data_type)

        range_filter_list_response = cls(
            filter_id=filter_id,
            title=title,
            description=description,
            type=type,
            question=question,
            min_=min_,
            max_=max_,
            data_type=data_type,
        )

        range_filter_list_response.additional_properties = d
        return range_filter_list_response

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
