from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SendMessage")


@attr.s(auto_attribs=True)
class SendMessage:
    """
    Attributes:
        recipient_id (str): Recipient user's id
        body (str): Message Body. Text is sanitised for safe storage and display.
        study_id (str): This study is the reason for this message
    """

    recipient_id: str
    body: str
    study_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        recipient_id = self.recipient_id
        body = self.body
        study_id = self.study_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipient_id": recipient_id,
                "body": body,
                "study_id": study_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        recipient_id = d.pop("recipient_id")

        body = d.pop("body")

        study_id = d.pop("study_id")

        send_message = cls(
            recipient_id=recipient_id,
            body=body,
            study_id=study_id,
        )

        send_message.additional_properties = d
        return send_message

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
