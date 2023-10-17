from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.invitation_status import InvitationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="Invitation")


@attr.s(auto_attribs=True)
class Invitation:
    """
    Attributes:
        association (Union[Unset, str]): The ID of the workspace or project to which the invitee was invited.
        invitee (Union[Unset, InvitationInvitee]):
        invited_by (Union[Unset, str]): The ID of the user who sent the invitation.
        status (Union[Unset, InvitationStatus]): The current status of the invitation.
        invite_link (Union[Unset, str]): The link that the invitee can use to accept the invitation.
    """

    association: Union[Unset, str] = UNSET
    invitee: Union[Unset, "InvitationInvitee"] = UNSET
    invited_by: Union[Unset, str] = UNSET
    status: Union[Unset, InvitationStatus] = UNSET
    invite_link: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        association = self.association
        invitee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.invitee, Unset):
            invitee = self.invitee.to_dict()

        invited_by = self.invited_by
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        invite_link = self.invite_link

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if association is not UNSET:
            field_dict["association"] = association
        if invitee is not UNSET:
            field_dict["invitee"] = invitee
        if invited_by is not UNSET:
            field_dict["invited_by"] = invited_by
        if status is not UNSET:
            field_dict["status"] = status
        if invite_link is not UNSET:
            field_dict["invite_link"] = invite_link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.invitation_invitee import InvitationInvitee

        d = src_dict.copy()
        association = d.pop("association", UNSET)

        _invitee = d.pop("invitee", UNSET)
        invitee: Union[Unset, InvitationInvitee]
        if isinstance(_invitee, Unset):
            invitee = UNSET
        else:
            invitee = InvitationInvitee.from_dict(_invitee)

        invited_by = d.pop("invited_by", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, InvitationStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = InvitationStatus(_status)

        invite_link = d.pop("invite_link", UNSET)

        invitation = cls(
            association=association,
            invitee=invitee,
            invited_by=invited_by,
            status=status,
            invite_link=invite_link,
        )

        invitation.additional_properties = d
        return invitation

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
