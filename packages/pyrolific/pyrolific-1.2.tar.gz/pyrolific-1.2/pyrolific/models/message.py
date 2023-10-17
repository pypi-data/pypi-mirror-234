import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Message")


@attr.s(auto_attribs=True)
class Message:
    """
    Attributes:
        sender_id (str): Id of the user who sent the message
        body (str): Body of the message.
        sent_at (datetime.datetime): Date time when message was sent
        channel_id (str): The channel ID, for linking back to a thread in the Prolific app. Example:
            d45c8a5e812ff990fc6546beaf888c9820f4c184f7200a45d900cf0f321f7f38.
        type (Union[Unset, str]): Will only me message for now
    """

    sender_id: str
    body: str
    sent_at: datetime.datetime
    channel_id: str
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sender_id = self.sender_id
        body = self.body
        sent_at = self.sent_at.isoformat()

        channel_id = self.channel_id
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sender_id": sender_id,
                "body": body,
                "sent_at": sent_at,
                "channel_id": channel_id,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sender_id = d.pop("sender_id")

        body = d.pop("body")

        sent_at = isoparse(d.pop("sent_at"))

        channel_id = d.pop("channel_id")

        type = d.pop("type", UNSET)

        message = cls(
            sender_id=sender_id,
            body=body,
            sent_at=sent_at,
            channel_id=channel_id,
            type=type,
        )

        message.additional_properties = d
        return message

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
