from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="CreateInvitationResponse")


@attr.s(auto_attribs=True)
class CreateInvitationResponse:
    """
    Attributes:
        invitations (Union[Unset, List['Invitation']]):
    """

    invitations: Union[Unset, List["Invitation"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        invitations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.invitations, Unset):
            invitations = []
            for invitations_item_data in self.invitations:
                invitations_item = invitations_item_data.to_dict()

                invitations.append(invitations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if invitations is not UNSET:
            field_dict["invitations"] = invitations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.invitation import Invitation

        d = src_dict.copy()
        invitations = []
        _invitations = d.pop("invitations", UNSET)
        for invitations_item_data in _invitations or []:
            invitations_item = Invitation.from_dict(invitations_item_data)

            invitations.append(invitations_item)

        create_invitation_response = cls(
            invitations=invitations,
        )

        create_invitation_response.additional_properties = d
        return create_invitation_response

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
