from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="ParticipantGroup")


@attr.s(auto_attribs=True)
class ParticipantGroup:
    """
    Attributes:
        id (Union[Unset, str]): The id of the participant group Example: 5e9b9c9b0f9c9a0001b0b1f5.
        name (Union[Unset, str]): The name of the participant group Example: Group 1.
        project_id (Union[Unset, str]): The id of the project the participant group belongs to Example:
            5e9b9c9b0f9c9a0001b0b1f4.
        participant_count (Union[Unset, int]): The number of participants in the participant group Example: 10.
        is_deleted (Union[Unset, bool]): Whether the participant group has been deleted
        feeder_studies (Union[Unset, List['ParticipantGroupFeederStudiesItem']]): Details of all studies which are
            configured to modify the participants in this group through completion codes.
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    participant_count: Union[Unset, int] = UNSET
    is_deleted: Union[Unset, bool] = UNSET
    feeder_studies: Union[Unset, List["ParticipantGroupFeederStudiesItem"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        project_id = self.project_id
        participant_count = self.participant_count
        is_deleted = self.is_deleted
        feeder_studies: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.feeder_studies, Unset):
            feeder_studies = []
            for feeder_studies_item_data in self.feeder_studies:
                feeder_studies_item = feeder_studies_item_data.to_dict()

                feeder_studies.append(feeder_studies_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if participant_count is not UNSET:
            field_dict["participant_count"] = participant_count
        if is_deleted is not UNSET:
            field_dict["is_deleted"] = is_deleted
        if feeder_studies is not UNSET:
            field_dict["feeder_studies"] = feeder_studies

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.participant_group_feeder_studies_item import ParticipantGroupFeederStudiesItem

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        project_id = d.pop("project_id", UNSET)

        participant_count = d.pop("participant_count", UNSET)

        is_deleted = d.pop("is_deleted", UNSET)

        feeder_studies = []
        _feeder_studies = d.pop("feeder_studies", UNSET)
        for feeder_studies_item_data in _feeder_studies or []:
            feeder_studies_item = ParticipantGroupFeederStudiesItem.from_dict(feeder_studies_item_data)

            feeder_studies.append(feeder_studies_item)

        participant_group = cls(
            id=id,
            name=name,
            project_id=project_id,
            participant_count=participant_count,
            is_deleted=is_deleted,
            feeder_studies=feeder_studies,
        )

        participant_group.additional_properties = d
        return participant_group

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
