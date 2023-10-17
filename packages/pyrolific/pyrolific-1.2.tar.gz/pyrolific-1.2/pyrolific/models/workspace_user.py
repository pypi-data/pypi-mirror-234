from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceUser")


@attr.s(auto_attribs=True)
class WorkspaceUser:
    """
    Attributes:
        id (str): Id of user
        name (Union[Unset, str]): Name of user
        email (Union[Unset, str]): email of user
        roles (Union[Unset, List[str]]): User roles in workspace
    """

    id: str
    name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    roles: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        email = self.email
        roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if email is not UNSET:
            field_dict["email"] = email
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        email = d.pop("email", UNSET)

        roles = cast(List[str], d.pop("roles", UNSET))

        workspace_user = cls(
            id=id,
            name=name,
            email=email,
            roles=roles,
        )

        workspace_user.additional_properties = d
        return workspace_user

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
