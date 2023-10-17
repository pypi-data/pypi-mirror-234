from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubscriptionDetail")


@attr.s(auto_attribs=True)
class SubscriptionDetail:
    """
    Attributes:
        event_type (str): The name of the event type associated to the subscription.
        target_url (str): The URL that the subscription will notify when your event type is triggered.
        workspace_id (str): The ID of the workspace we will create the subscription in.
        id (Union[Unset, str]): The ID of the subscription.
        is_enabled (Union[Unset, bool]): Whether the subscription is enabled or not.
    """

    event_type: str
    target_url: str
    workspace_id: str
    id: Union[Unset, str] = UNSET
    is_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event_type = self.event_type
        target_url = self.target_url
        workspace_id = self.workspace_id
        id = self.id
        is_enabled = self.is_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
                "target_url": target_url,
                "workspace_id": workspace_id,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        event_type = d.pop("event_type")

        target_url = d.pop("target_url")

        workspace_id = d.pop("workspace_id")

        id = d.pop("id", UNSET)

        is_enabled = d.pop("is_enabled", UNSET)

        subscription_detail = cls(
            event_type=event_type,
            target_url=target_url,
            workspace_id=workspace_id,
            id=id,
            is_enabled=is_enabled,
        )

        subscription_detail.additional_properties = d
        return subscription_detail

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
