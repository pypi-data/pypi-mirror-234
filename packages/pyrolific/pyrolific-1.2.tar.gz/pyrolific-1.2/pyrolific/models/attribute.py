from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="Attribute")


@attr.s(auto_attribs=True)
class Attribute:
    """
    Attributes:
        value (Union['AttributeValueType0', List[Union['AttributeValueType1ItemType1', str]], bool, float, str]):
            Attribute value. It can be null, a number, a date or a boolean depending on the type of requirement.
            For boolean values, there is no need to specify all false (non selected) options. Example: true.
        index (Union[Unset, float]): Attribute index. It is mandatory for some type of requirements,
            like SelectAnswerEligibilityRequirement. Example: 5.0.
        name (Union[Unset, str]): Attribute name. It is mandatory for some type of requirements,
            like AgeRangeEligibilityRequirement.
    """

    value: Union["AttributeValueType0", List[Union["AttributeValueType1ItemType1", str]], bool, float, str]
    index: Union[Unset, float] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.attribute_value_type_0 import AttributeValueType0
        from ..models.attribute_value_type_1_item_type_1 import AttributeValueType1ItemType1

        value: Union[Dict[str, Any], List[Union[Dict[str, Any], str]], bool, float, str]

        if isinstance(self.value, AttributeValueType0):
            value = self.value.to_dict() if self.value else None

        elif isinstance(self.value, list):
            if self.value is None:
                value = None
            else:
                value = []
                for value_type_1_item_data in self.value:
                    value_type_1_item: Union[Dict[str, Any], str]

                    if isinstance(value_type_1_item_data, AttributeValueType1ItemType1):
                        value_type_1_item = value_type_1_item_data.to_dict()

                    else:
                        value_type_1_item = value_type_1_item_data

                    value.append(value_type_1_item)

        else:
            value = self.value

        index = self.index
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if index is not UNSET:
            field_dict["index"] = index
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.attribute_value_type_0 import AttributeValueType0
        from ..models.attribute_value_type_1_item_type_1 import AttributeValueType1ItemType1

        d = src_dict.copy()

        def _parse_value(
            data: object,
        ) -> Union["AttributeValueType0", List[Union["AttributeValueType1ItemType1", str]], bool, float, str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _value_type_0 = data
                value_type_0: Optional[AttributeValueType0]
                if _value_type_0 is None:
                    value_type_0 = UNSET
                else:
                    value_type_0 = AttributeValueType0.from_dict(_value_type_0)

                return value_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = UNSET
                _value_type_1 = data
                for value_type_1_item_data in _value_type_1 or []:

                    def _parse_value_type_1_item(data: object) -> Union["AttributeValueType1ItemType1", str]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_1_item_type_1 = AttributeValueType1ItemType1.from_dict(data)

                            return value_type_1_item_type_1
                        except:  # noqa: E722
                            pass
                        return cast(Union["AttributeValueType1ItemType1", str], data)

                    value_type_1_item = _parse_value_type_1_item(value_type_1_item_data)

                    value_type_1.append(value_type_1_item)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union["AttributeValueType0", List[Union["AttributeValueType1ItemType1", str]], bool, float, str], data
            )

        value = _parse_value(d.pop("value"))

        index = d.pop("index", UNSET)

        name = d.pop("name", UNSET)

        attribute = cls(
            value=value,
            index=index,
            name=name,
        )

        attribute.additional_properties = d
        return attribute

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
