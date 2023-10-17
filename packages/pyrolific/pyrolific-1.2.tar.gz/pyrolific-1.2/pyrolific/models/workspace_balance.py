from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="WorkspaceBalance")


@attr.s(auto_attribs=True)
class WorkspaceBalance:
    """
    Example:
        {'currency_code': 'GBP', 'total_balance': 630, 'balance_breakdown': {'rewards': 450, 'fees': 150, 'vat': 30},
            'available_balance': 210, 'available_balance_breakdown': {'rewards': 150, 'fees': 50, 'vat': 10}}

    Attributes:
        currency_code (Union[Unset, str]): The currency used for all financial transactions within the workspace.
        total_balance (Union[Unset, int]): The total balance of the workspace, including funds which have already been
            assigned to active studies.

            All monetary values are shown in the sub-currency of your workspace currency (e.g. pence, cents).
        balance_breakdown (Union[Unset, WorkspaceBalanceBalanceBreakdown]): A breakdown of the total balance of the
            workspace into:
            - Funds available to pay to participants
            - Funds pre-paid to Prolific for our services
            - Funds for any VAT applied to our service fees
        available_balance (Union[Unset, int]): The remaining balance of your workspace which is available to spend,
            after removing funds assigned to already active studies, etc.
        available_balance_breakdown (Union[Unset, WorkspaceBalanceAvailableBalanceBreakdown]): A breakdown of the
            available balance of the workspace into:
            - Funds available to pay to participants
            - Funds pre-paid to Prolific for our services
            - Funds for any VAT applied to our service fees
    """

    currency_code: Union[Unset, str] = UNSET
    total_balance: Union[Unset, int] = UNSET
    balance_breakdown: Union[Unset, "WorkspaceBalanceBalanceBreakdown"] = UNSET
    available_balance: Union[Unset, int] = UNSET
    available_balance_breakdown: Union[Unset, "WorkspaceBalanceAvailableBalanceBreakdown"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency_code = self.currency_code
        total_balance = self.total_balance
        balance_breakdown: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.balance_breakdown, Unset):
            balance_breakdown = self.balance_breakdown.to_dict()

        available_balance = self.available_balance
        available_balance_breakdown: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.available_balance_breakdown, Unset):
            available_balance_breakdown = self.available_balance_breakdown.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if currency_code is not UNSET:
            field_dict["currency_code"] = currency_code
        if total_balance is not UNSET:
            field_dict["total_balance"] = total_balance
        if balance_breakdown is not UNSET:
            field_dict["balance_breakdown"] = balance_breakdown
        if available_balance is not UNSET:
            field_dict["available_balance"] = available_balance
        if available_balance_breakdown is not UNSET:
            field_dict["available_balance_breakdown"] = available_balance_breakdown

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_balance_available_balance_breakdown import WorkspaceBalanceAvailableBalanceBreakdown
        from ..models.workspace_balance_balance_breakdown import WorkspaceBalanceBalanceBreakdown

        d = src_dict.copy()
        currency_code = d.pop("currency_code", UNSET)

        total_balance = d.pop("total_balance", UNSET)

        _balance_breakdown = d.pop("balance_breakdown", UNSET)
        balance_breakdown: Union[Unset, WorkspaceBalanceBalanceBreakdown]
        if isinstance(_balance_breakdown, Unset):
            balance_breakdown = UNSET
        else:
            balance_breakdown = WorkspaceBalanceBalanceBreakdown.from_dict(_balance_breakdown)

        available_balance = d.pop("available_balance", UNSET)

        _available_balance_breakdown = d.pop("available_balance_breakdown", UNSET)
        available_balance_breakdown: Union[Unset, WorkspaceBalanceAvailableBalanceBreakdown]
        if isinstance(_available_balance_breakdown, Unset):
            available_balance_breakdown = UNSET
        else:
            available_balance_breakdown = WorkspaceBalanceAvailableBalanceBreakdown.from_dict(
                _available_balance_breakdown
            )

        workspace_balance = cls(
            currency_code=currency_code,
            total_balance=total_balance,
            balance_breakdown=balance_breakdown,
            available_balance=available_balance,
            available_balance_breakdown=available_balance_breakdown,
        )

        workspace_balance.additional_properties = d
        return workspace_balance

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
