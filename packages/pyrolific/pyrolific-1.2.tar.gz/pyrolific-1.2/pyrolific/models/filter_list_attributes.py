from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.filter_list_attributes_type import FilterListAttributesType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterListAttributes")


@attr.s(auto_attribs=True)
class FilterListAttributes:
    """
    Attributes:
        filter_id (Union[Unset, str]): The ID of the filter, based on a slugified version of the title at the time the
            filter was created.
        title (Union[Unset, str]): The title of the filter.
        description (Union[Unset, str]): A description of the filter.
        type (Union[Unset, FilterListAttributesType]): The filter type.
        question (Union[Unset, str]): The question asked of participants to generate this filter.
    """

    filter_id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type: Union[Unset, FilterListAttributesType] = UNSET
    question: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_id = self.filter_id
        title = self.title
        description = self.description
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        question = self.question

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

        filter_list_attributes = cls(
            filter_id=filter_id,
            title=title,
            description=description,
            type=type,
            question=question,
        )

        filter_list_attributes.additional_properties = d
        return filter_list_attributes

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
