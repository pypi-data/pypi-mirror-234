from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.select_filter_list_attributes_data_type import SelectFilterListAttributesDataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="SelectFilterListAttributes")


@attr.s(auto_attribs=True)
class SelectFilterListAttributes:
    """
    Attributes:
        choices (Union[Unset, SelectFilterListAttributesChoices]): An object containing all the filter's possible
            responses as key-value pairs, with sequential integer IDs or database ObjectIDs as the keys and the text of the
            response as the values.
        data_type (Union[Unset, SelectFilterListAttributesDataType]): The format of the keys in the choices object. If
            the keys are strings representing sequential integers,
            the data format is integer. If the keys are database ObjectIDs, the type of ID is specified.
    """

    choices: Union[Unset, "SelectFilterListAttributesChoices"] = UNSET
    data_type: Union[Unset, SelectFilterListAttributesDataType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        choices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = self.choices.to_dict()

        data_type: Union[Unset, str] = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = self.data_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if choices is not UNSET:
            field_dict["choices"] = choices
        if data_type is not UNSET:
            field_dict["data_type"] = data_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.select_filter_list_attributes_choices import SelectFilterListAttributesChoices

        d = src_dict.copy()
        _choices = d.pop("choices", UNSET)
        choices: Union[Unset, SelectFilterListAttributesChoices]
        if isinstance(_choices, Unset):
            choices = UNSET
        else:
            choices = SelectFilterListAttributesChoices.from_dict(_choices)

        _data_type = d.pop("data_type", UNSET)
        data_type: Union[Unset, SelectFilterListAttributesDataType]
        if isinstance(_data_type, Unset):
            data_type = UNSET
        else:
            data_type = SelectFilterListAttributesDataType(_data_type)

        select_filter_list_attributes = cls(
            choices=choices,
            data_type=data_type,
        )

        select_filter_list_attributes.additional_properties = d
        return select_filter_list_attributes

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
