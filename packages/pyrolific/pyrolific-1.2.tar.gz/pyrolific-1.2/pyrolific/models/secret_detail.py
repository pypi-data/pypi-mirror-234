from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SecretDetail")


@attr.s(auto_attribs=True)
class SecretDetail:
    """
    Example:
        {'id': '63722971f9cc073ecc730f6a', 'value': 'cGNqFPb6y0RT3XO9XVSessBDYIbHQ-....', 'workspace_id':
            '63722982f9cc073ecc730f6b'}

    Attributes:
        id (Union[Unset, str]): The ID of the secret.
        value (Union[Unset, str]): The secret value.
        workspace_id (Union[Unset, str]): The ID of the workspace that the secret belongs to.
    """

    id: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if value is not UNSET:
            field_dict["value"] = value
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        value = d.pop("value", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        secret_detail = cls(
            id=id,
            value=value,
            workspace_id=workspace_id,
        )

        secret_detail.additional_properties = d
        return secret_detail

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
