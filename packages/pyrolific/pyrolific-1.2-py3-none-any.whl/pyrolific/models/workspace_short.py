from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="WorkspaceShort")


@attr.s(auto_attribs=True)
class WorkspaceShort:
    """
    Example:
        {'id': '62fce6fff0a78eb4f3ebc09c', 'title': 'My workspace', 'description': 'This workspace does...', 'owner':
            '60a42f4c693c29420793cb73', 'users': [{'id': '60a42f4c693c29420793cb73', 'name': 'Joe Soap', 'email':
            'joe.soap@gmail.com', 'roles': ['WORKSPACE_ADMIN']}], 'naivety_distribution_rate': 0.5}

    Attributes:
        id (str): Workspace id. It is created by Prolific.
        title (str): Name of workspace
        description (Union[Unset, str]): What is this workspace used for
        owner (Union[Unset, str]): User id of the creator of the workspace. It is created by Prolific.
        users (Union[Unset, List['WorkspaceUser']]): Data for all users who have access to this workspace
        naivety_distribution_rate (Union[Unset, None, float]): The rate at which the studies within this project are
            distributed.
    """

    id: str
    title: str
    description: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    users: Union[Unset, List["WorkspaceUser"]] = UNSET
    naivety_distribution_rate: Union[Unset, None, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        title = self.title
        description = self.description
        owner = self.owner
        users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()

                users.append(users_item)

        naivety_distribution_rate = self.naivety_distribution_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if owner is not UNSET:
            field_dict["owner"] = owner
        if users is not UNSET:
            field_dict["users"] = users
        if naivety_distribution_rate is not UNSET:
            field_dict["naivety_distribution_rate"] = naivety_distribution_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_user import WorkspaceUser

        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        description = d.pop("description", UNSET)

        owner = d.pop("owner", UNSET)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = WorkspaceUser.from_dict(users_item_data)

            users.append(users_item)

        naivety_distribution_rate = d.pop("naivety_distribution_rate", UNSET)

        workspace_short = cls(
            id=id,
            title=title,
            description=description,
            owner=owner,
            users=users,
            naivety_distribution_rate=naivety_distribution_rate,
        )

        workspace_short.additional_properties = d
        return workspace_short

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
