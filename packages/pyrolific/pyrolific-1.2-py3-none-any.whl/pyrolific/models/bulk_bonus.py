from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkBonus")


@attr.s(auto_attribs=True)
class BulkBonus:
    """
    Example:
        {'id': '621014cb8e9e0f81e387021f', 'study': '620ca2735fcbba4fa2b3211a', 'amount': 850, 'fees': 283.34, 'vat': 0,
            'total_amount': 1133.34}

    Attributes:
        id (str): Bonus ID. It is the ID to be used when paying the bonus
        total_amount (float): Total ammount that will be deducted from your balance in cents
        study (Union[Unset, str]): Study ID
        amount (Union[Unset, float]): The amount the participant will receive in cents
        fees (Union[Unset, float]): The fees Prolific will charge for this bonus in cents
        vat (Union[Unset, float]): The VAT cost for this bonus in cents
    """

    id: str
    total_amount: float
    study: Union[Unset, str] = UNSET
    amount: Union[Unset, float] = UNSET
    fees: Union[Unset, float] = UNSET
    vat: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        total_amount = self.total_amount
        study = self.study
        amount = self.amount
        fees = self.fees
        vat = self.vat

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "total_amount": total_amount,
            }
        )
        if study is not UNSET:
            field_dict["study"] = study
        if amount is not UNSET:
            field_dict["amount"] = amount
        if fees is not UNSET:
            field_dict["fees"] = fees
        if vat is not UNSET:
            field_dict["vat"] = vat

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        total_amount = d.pop("total_amount")

        study = d.pop("study", UNSET)

        amount = d.pop("amount", UNSET)

        fees = d.pop("fees", UNSET)

        vat = d.pop("vat", UNSET)

        bulk_bonus = cls(
            id=id,
            total_amount=total_amount,
            study=study,
            amount=amount,
            fees=fees,
            vat=vat,
        )

        bulk_bonus.additional_properties = d
        return bulk_bonus

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
