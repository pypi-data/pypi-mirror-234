from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.base_study_completion_option import BaseStudyCompletionOption
from ..models.base_study_device_compatibility_item import BaseStudyDeviceCompatibilityItem
from ..models.base_study_peripheral_requirements_item import BaseStudyPeripheralRequirementsItem
from ..models.base_study_prolific_id_option import BaseStudyProlificIdOption
from ..types import UNSET, Unset

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="BaseStudy")


@attr.s(auto_attribs=True)
class BaseStudy:
    r"""
    Attributes:
        name (Union[Unset, str]): Public name or title of the study
        internal_name (Union[Unset, None, str]): Internal name of the study, not shown to participants
        description (Union[Unset, str]): Description of the study for the participants to read before
            starting the study
        external_study_url (Union[Unset, str]): URL of the survey or experiment you want participant to access. You can
            pass URL search parameters to your survey or experiment

            * Participant id {{%PROLIFIC_PID%}}
            * Study id {{%STUDY_ID%}}
            * Session id {{%SESSION_ID%}}

            For example `https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}`
        prolific_id_option (Union[Unset, BaseStudyProlificIdOption]): Use 'question' if you will add a question in your
            survey or experiment asking the participant ID

            **Recommended** Use 'url_parameters' if your survey or experiment can retrieve and store those parameters for
            your analysis.

            Use 'not_required' if you don't need to record them
        completion_option (Union[Unset, BaseStudyCompletionOption]): Use 'url' if you will redirect the user back to
            prolific using a url,
            the url you will use in your experiment
            or survey to go back is https://app.prolific.com/submissions/complete?cc={code}

            Use 'code' when the participants will manually input the code, at the
            end of the experiment you will tell the participants the code. Note that
            the {code} you have to give is one of the completion codes you define below in the `completion_codes` argument.
        completion_codes (Union[Unset, List['BaseStudyCompletionCodesItem']]): Specify at least one completion code for
            your study. A participant will enter one of these codes when they complete your study.

            Each code must be unique within a study.

            You can specify as many actions as you like per code.
        total_available_places (Union[Unset, float]): How many participants are you looking to recruit
        estimated_completion_time (Union[Unset, float]): Estimated duration in minutes of the experiment or survey
        maximum_allowed_time (Union[Unset, float]): Max time in minutes for a participant to finish the submission.
            Submissions are timed out if it takes longer.

            If it is not provided the default value is set to the max value.

            The min value is calculated as two minutes plus two times the estimated time plus two times the square root of
            the estimated time
        reward (Union[Unset, float]): How much are you going to pay the participants in cents. We
            use the currency of your account.
        device_compatibility (Union[Unset, List[BaseStudyDeviceCompatibilityItem]]): Add all devices that participants
            can use.
            You can include one or more options.

            An empty array indicates that all options are available.
        peripheral_requirements (Union[Unset, List[BaseStudyPeripheralRequirementsItem]]): Add all requirements that
            participants have to meet.

            An empty array indicates that there are no extra peripheral requirements.
        filters (Union[Unset, None, List[Union['RangeFilter', 'SelectFilter']]]): Array of filters.

            Use empty array for "Everyone"
        filter_set_id (Union[Unset, None, str]): The ID of a filter set, from which filters for the study will be taken.

            Note, this cannot be used in combination with additional filters via the `filters` field.
        filter_set_version (Union[Unset, None, int]): The version of the filter set to be used.

            If not provided, this will default to the latest available version at the time of applying the filter set.
        naivety_distribution_rate (Union[Unset, None, float]): Control the balance between speed of your studies and the
            naivety of the participants.

            If not defined, by default Prolific calculates the best rate for most studies
            taking into account the `filters` and the `total_available_places` needed for this study.

            Use 0 if your priority is speed. When this property is set to 0 all eligible participants will have access
            to your study at the same time, without any prioritization.

            You can also set this at a workspace and project level.
        project (Union[Unset, str]): Project id, this is optional and if not supplied with be the put in the default
            workspace and project.
        submissions_config (Union[Unset, BaseStudySubmissionsConfig]): **BETA**: This is a beta feature and is currently
            only available to selected workspaces.
            It is being tested and evaluated for effectiveness and user experience before being released to all users.

            **Advanced**: This helps with faster data collection. Your survey system will need to handle providing a
            unique experience each time the participant takes the study.

            Configuration related to study submissions. The purpose of this field is to capture any configuration options
            that impact the submissions made by participants in a study.
        metadata (Union[Unset, None, str]): This field can be used to store extra information required for a system
            integration.
            For example, it could be some JSON, XML, an integer, or a string.

            Examples could include:

              - `123345` - An ID from your system, that helps with linkage when returning the study.
              - `{ \"id\": \"45\", \"type\": \"finance\"}` - Some JSON that you want to store.
    """

    name: Union[Unset, str] = UNSET
    internal_name: Union[Unset, None, str] = UNSET
    description: Union[Unset, str] = UNSET
    external_study_url: Union[Unset, str] = UNSET
    prolific_id_option: Union[Unset, BaseStudyProlificIdOption] = UNSET
    completion_option: Union[Unset, BaseStudyCompletionOption] = UNSET
    completion_codes: Union[Unset, List["BaseStudyCompletionCodesItem"]] = UNSET
    total_available_places: Union[Unset, float] = UNSET
    estimated_completion_time: Union[Unset, float] = UNSET
    maximum_allowed_time: Union[Unset, float] = UNSET
    reward: Union[Unset, float] = UNSET
    device_compatibility: Union[Unset, List[BaseStudyDeviceCompatibilityItem]] = UNSET
    peripheral_requirements: Union[Unset, List[BaseStudyPeripheralRequirementsItem]] = UNSET
    filters: Union[Unset, None, List[Union["RangeFilter", "SelectFilter"]]] = UNSET
    filter_set_id: Union[Unset, None, str] = UNSET
    filter_set_version: Union[Unset, None, int] = UNSET
    naivety_distribution_rate: Union[Unset, None, float] = UNSET
    project: Union[Unset, str] = UNSET
    submissions_config: Union[Unset, "BaseStudySubmissionsConfig"] = UNSET
    metadata: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.select_filter import SelectFilter

        name = self.name
        internal_name = self.internal_name
        description = self.description
        external_study_url = self.external_study_url
        prolific_id_option: Union[Unset, str] = UNSET
        if not isinstance(self.prolific_id_option, Unset):
            prolific_id_option = self.prolific_id_option.value

        completion_option: Union[Unset, str] = UNSET
        if not isinstance(self.completion_option, Unset):
            completion_option = self.completion_option.value

        completion_codes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.completion_codes, Unset):
            completion_codes = []
            for completion_codes_item_data in self.completion_codes:
                completion_codes_item = completion_codes_item_data.to_dict()

                completion_codes.append(completion_codes_item)

        total_available_places = self.total_available_places
        estimated_completion_time = self.estimated_completion_time
        maximum_allowed_time = self.maximum_allowed_time
        reward = self.reward
        device_compatibility: Union[Unset, List[str]] = UNSET
        if not isinstance(self.device_compatibility, Unset):
            device_compatibility = []
            for device_compatibility_item_data in self.device_compatibility:
                device_compatibility_item = device_compatibility_item_data.value

                device_compatibility.append(device_compatibility_item)

        peripheral_requirements: Union[Unset, List[str]] = UNSET
        if not isinstance(self.peripheral_requirements, Unset):
            peripheral_requirements = []
            for peripheral_requirements_item_data in self.peripheral_requirements:
                peripheral_requirements_item = peripheral_requirements_item_data.value

                peripheral_requirements.append(peripheral_requirements_item)

        filters: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            if self.filters is None:
                filters = None
            else:
                filters = []
                for filters_item_data in self.filters:
                    filters_item: Dict[str, Any]

                    if isinstance(filters_item_data, SelectFilter):
                        filters_item = filters_item_data.to_dict()

                    else:
                        filters_item = filters_item_data.to_dict()

                    filters.append(filters_item)

        filter_set_id = self.filter_set_id
        filter_set_version = self.filter_set_version
        naivety_distribution_rate = self.naivety_distribution_rate
        project = self.project
        submissions_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.submissions_config, Unset):
            submissions_config = self.submissions_config.to_dict()

        metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if internal_name is not UNSET:
            field_dict["internal_name"] = internal_name
        if description is not UNSET:
            field_dict["description"] = description
        if external_study_url is not UNSET:
            field_dict["external_study_url"] = external_study_url
        if prolific_id_option is not UNSET:
            field_dict["prolific_id_option"] = prolific_id_option
        if completion_option is not UNSET:
            field_dict["completion_option"] = completion_option
        if completion_codes is not UNSET:
            field_dict["completion_codes"] = completion_codes
        if total_available_places is not UNSET:
            field_dict["total_available_places"] = total_available_places
        if estimated_completion_time is not UNSET:
            field_dict["estimated_completion_time"] = estimated_completion_time
        if maximum_allowed_time is not UNSET:
            field_dict["maximum_allowed_time"] = maximum_allowed_time
        if reward is not UNSET:
            field_dict["reward"] = reward
        if device_compatibility is not UNSET:
            field_dict["device_compatibility"] = device_compatibility
        if peripheral_requirements is not UNSET:
            field_dict["peripheral_requirements"] = peripheral_requirements
        if filters is not UNSET:
            field_dict["filters"] = filters
        if filter_set_id is not UNSET:
            field_dict["filter_set_id"] = filter_set_id
        if filter_set_version is not UNSET:
            field_dict["filter_set_version"] = filter_set_version
        if naivety_distribution_rate is not UNSET:
            field_dict["naivety_distribution_rate"] = naivety_distribution_rate
        if project is not UNSET:
            field_dict["project"] = project
        if submissions_config is not UNSET:
            field_dict["submissions_config"] = submissions_config
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_study_completion_codes_item import BaseStudyCompletionCodesItem
        from ..models.base_study_submissions_config import BaseStudySubmissionsConfig
        from ..models.range_filter import RangeFilter
        from ..models.select_filter import SelectFilter

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        internal_name = d.pop("internal_name", UNSET)

        description = d.pop("description", UNSET)

        external_study_url = d.pop("external_study_url", UNSET)

        _prolific_id_option = d.pop("prolific_id_option", UNSET)
        prolific_id_option: Union[Unset, BaseStudyProlificIdOption]
        if isinstance(_prolific_id_option, Unset):
            prolific_id_option = UNSET
        else:
            prolific_id_option = BaseStudyProlificIdOption(_prolific_id_option)

        _completion_option = d.pop("completion_option", UNSET)
        completion_option: Union[Unset, BaseStudyCompletionOption]
        if isinstance(_completion_option, Unset):
            completion_option = UNSET
        else:
            completion_option = BaseStudyCompletionOption(_completion_option)

        completion_codes = []
        _completion_codes = d.pop("completion_codes", UNSET)
        for completion_codes_item_data in _completion_codes or []:
            completion_codes_item = BaseStudyCompletionCodesItem.from_dict(completion_codes_item_data)

            completion_codes.append(completion_codes_item)

        total_available_places = d.pop("total_available_places", UNSET)

        estimated_completion_time = d.pop("estimated_completion_time", UNSET)

        maximum_allowed_time = d.pop("maximum_allowed_time", UNSET)

        reward = d.pop("reward", UNSET)

        device_compatibility = []
        _device_compatibility = d.pop("device_compatibility", UNSET)
        for device_compatibility_item_data in _device_compatibility or []:
            device_compatibility_item = BaseStudyDeviceCompatibilityItem(device_compatibility_item_data)

            device_compatibility.append(device_compatibility_item)

        peripheral_requirements = []
        _peripheral_requirements = d.pop("peripheral_requirements", UNSET)
        for peripheral_requirements_item_data in _peripheral_requirements or []:
            peripheral_requirements_item = BaseStudyPeripheralRequirementsItem(peripheral_requirements_item_data)

            peripheral_requirements.append(peripheral_requirements_item)

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(data: object) -> Union["RangeFilter", "SelectFilter"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = SelectFilter.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_1 = RangeFilter.from_dict(data)

                return filters_item_type_1

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        filter_set_id = d.pop("filter_set_id", UNSET)

        filter_set_version = d.pop("filter_set_version", UNSET)

        naivety_distribution_rate = d.pop("naivety_distribution_rate", UNSET)

        project = d.pop("project", UNSET)

        _submissions_config = d.pop("submissions_config", UNSET)
        submissions_config: Union[Unset, BaseStudySubmissionsConfig]
        if isinstance(_submissions_config, Unset):
            submissions_config = UNSET
        else:
            submissions_config = BaseStudySubmissionsConfig.from_dict(_submissions_config)

        metadata = d.pop("metadata", UNSET)

        base_study = cls(
            name=name,
            internal_name=internal_name,
            description=description,
            external_study_url=external_study_url,
            prolific_id_option=prolific_id_option,
            completion_option=completion_option,
            completion_codes=completion_codes,
            total_available_places=total_available_places,
            estimated_completion_time=estimated_completion_time,
            maximum_allowed_time=maximum_allowed_time,
            reward=reward,
            device_compatibility=device_compatibility,
            peripheral_requirements=peripheral_requirements,
            filters=filters,
            filter_set_id=filter_set_id,
            filter_set_version=filter_set_version,
            naivety_distribution_rate=naivety_distribution_rate,
            project=project,
            submissions_config=submissions_config,
            metadata=metadata,
        )

        base_study.additional_properties = d
        return base_study

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
