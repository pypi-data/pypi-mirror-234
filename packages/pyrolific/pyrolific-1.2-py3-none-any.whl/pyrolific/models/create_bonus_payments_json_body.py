from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateBonusPaymentsJsonBody")


@attr.s(auto_attribs=True)
class CreateBonusPaymentsJsonBody:
    r"""
    Example:
        {'study_id': '60f6acb180a7b59ac0621f9e', 'csv_bonuses':
            '60ffe5c8371090c7041d43f8,4.25\n60ff44a1d00991f1dfe405d9,4.25'}

    Attributes:
        study_id (Union[Unset, str]):
        csv_bonuses (Union[Unset, str]):
    """

    study_id: Union[Unset, str] = UNSET
    csv_bonuses: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        study_id = self.study_id
        csv_bonuses = self.csv_bonuses

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if study_id is not UNSET:
            field_dict["study_id"] = study_id
        if csv_bonuses is not UNSET:
            field_dict["csv_bonuses"] = csv_bonuses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        study_id = d.pop("study_id", UNSET)

        csv_bonuses = d.pop("csv_bonuses", UNSET)

        create_bonus_payments_json_body = cls(
            study_id=study_id,
            csv_bonuses=csv_bonuses,
        )

        create_bonus_payments_json_body.additional_properties = d
        return create_bonus_payments_json_body

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
