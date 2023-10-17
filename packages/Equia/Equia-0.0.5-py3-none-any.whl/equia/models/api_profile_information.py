from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_profile_time_information import ApiProfileTimeInformation
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiProfileInformation")


@attr.s(auto_attribs=True)
class ApiProfileInformation:
    """Holds profiling result"""

    profile_results: Union[Unset, None, List[ApiProfileTimeInformation]] = UNSET
    total_milli_seconds: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        profile_results: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.profile_results, Unset):
            if self.profile_results is None:
                profile_results = None
            else:
                profile_results = []
                for profile_results_item_data in self.profile_results:
                    profile_results_item = profile_results_item_data.to_dict()

                    profile_results.append(profile_results_item)

        total_milli_seconds = self.total_milli_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if profile_results is not UNSET:
            field_dict["profileResults"] = profile_results
        if total_milli_seconds is not UNSET:
            field_dict["totalMilliSeconds"] = total_milli_seconds

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        profile_results = []
        _profile_results = d.pop("profileResults", UNSET)
        for profile_results_item_data in _profile_results or []:
            profile_results_item = ApiProfileTimeInformation.from_dict(profile_results_item_data)

            profile_results.append(profile_results_item)

        total_milli_seconds = d.pop("totalMilliSeconds", UNSET)

        api_profile_information = cls(
            profile_results=profile_results,
            total_milli_seconds=total_milli_seconds,
        )

        return api_profile_information
