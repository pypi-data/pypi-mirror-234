from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="StudyCostRequest")


@attr.s(auto_attribs=True)
class StudyCostRequest:
    """
    Attributes:
        reward (float): How much are you going to pay the participants in cents. We use the currency of your account
        total_available_places (float): How many participants are you looking to recruit
    """

    reward: float
    total_available_places: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reward = self.reward
        total_available_places = self.total_available_places

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reward": reward,
                "total_available_places": total_available_places,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reward = d.pop("reward")

        total_available_places = d.pop("total_available_places")

        study_cost_request = cls(
            reward=reward,
            total_available_places=total_available_places,
        )

        study_cost_request.additional_properties = d
        return study_cost_request

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
