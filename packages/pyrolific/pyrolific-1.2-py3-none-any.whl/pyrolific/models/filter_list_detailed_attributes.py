from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FilterListDetailedAttributes")


@attr.s(auto_attribs=True)
class FilterListDetailedAttributes:
    """
    Attributes:
        researcher_help_text (Union[Unset, None, str]): Some help text to be displayed to researchers in the
            prescreening modal.
        participant_help_text (Union[Unset, None, str]): Some help text to be displayed to participants in the About You
            section.
        category (Union[Unset, None, str]): The category the filter is displayed in in About You and the prescreening
            modal.
        subcategory (Union[Unset, None, str]): The sub-category the filter is displayed in in the prescreening modal.
        display_order (Union[Unset, None, int]): The order in which the filter is displayed within its sub-category in
            the prescreening modal.
        tags (Union[Unset, None, List[str]]): Some additional tags that can be used to display the filter in a specific
            way, e.g. recommended, new, expiring.
    """

    researcher_help_text: Union[Unset, None, str] = UNSET
    participant_help_text: Union[Unset, None, str] = UNSET
    category: Union[Unset, None, str] = UNSET
    subcategory: Union[Unset, None, str] = UNSET
    display_order: Union[Unset, None, int] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        researcher_help_text = self.researcher_help_text
        participant_help_text = self.participant_help_text
        category = self.category
        subcategory = self.subcategory
        display_order = self.display_order
        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if researcher_help_text is not UNSET:
            field_dict["researcher_help_text"] = researcher_help_text
        if participant_help_text is not UNSET:
            field_dict["participant_help_text"] = participant_help_text
        if category is not UNSET:
            field_dict["category"] = category
        if subcategory is not UNSET:
            field_dict["subcategory"] = subcategory
        if display_order is not UNSET:
            field_dict["display_order"] = display_order
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        researcher_help_text = d.pop("researcher_help_text", UNSET)

        participant_help_text = d.pop("participant_help_text", UNSET)

        category = d.pop("category", UNSET)

        subcategory = d.pop("subcategory", UNSET)

        display_order = d.pop("display_order", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        filter_list_detailed_attributes = cls(
            researcher_help_text=researcher_help_text,
            participant_help_text=participant_help_text,
            category=category,
            subcategory=subcategory,
            display_order=display_order,
            tags=tags,
        )

        filter_list_detailed_attributes.additional_properties = d
        return filter_list_detailed_attributes

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
