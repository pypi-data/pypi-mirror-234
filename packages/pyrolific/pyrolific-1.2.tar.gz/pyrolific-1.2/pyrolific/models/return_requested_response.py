import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.return_requested_response_status import ReturnRequestedResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReturnRequestedResponse")


@attr.s(auto_attribs=True)
class ReturnRequestedResponse:
    """
    Attributes:
        id (Union[Unset, str]): the database id of the submission instance
        status (Union[Unset, ReturnRequestedResponseStatus]): The current status of the submission
        participant (Union[Unset, str]): The participant who took part in the study.
        return_requested (Union[Unset, None, datetime.datetime]): The date and time when a request was made to return a
            submission.
    """

    id: Union[Unset, str] = UNSET
    status: Union[Unset, ReturnRequestedResponseStatus] = UNSET
    participant: Union[Unset, str] = UNSET
    return_requested: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        participant = self.participant
        return_requested: Union[Unset, None, str] = UNSET
        if not isinstance(self.return_requested, Unset):
            return_requested = self.return_requested.isoformat() if self.return_requested else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if participant is not UNSET:
            field_dict["participant"] = participant
        if return_requested is not UNSET:
            field_dict["return_requested"] = return_requested

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ReturnRequestedResponseStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ReturnRequestedResponseStatus(_status)

        participant = d.pop("participant", UNSET)

        _return_requested = d.pop("return_requested", UNSET)
        return_requested: Union[Unset, None, datetime.datetime]
        if _return_requested is None:
            return_requested = None
        elif isinstance(_return_requested, Unset):
            return_requested = UNSET
        else:
            return_requested = isoparse(_return_requested)

        return_requested_response = cls(
            id=id,
            status=status,
            participant=participant,
            return_requested=return_requested,
        )

        return_requested_response.additional_properties = d
        return return_requested_response

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
