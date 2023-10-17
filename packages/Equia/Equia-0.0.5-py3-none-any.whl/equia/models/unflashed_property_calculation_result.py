from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_output_unflashed_property_result import ApiOutputUnflashedPropertyResult
from ..models.api_profile_information import ApiProfileInformation
from ..models.exception_info import ExceptionInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="UnflashedPropertyCalculationResult")


@attr.s(auto_attribs=True)
class UnflashedPropertyCalculationResult:
    """Holds calculation result for a point"""

    success: Union[Unset, bool] = UNSET
    calculation_id: Union[Unset, None, str] = UNSET
    exception_info: Union[Unset, ExceptionInfo] = UNSET
    profiling: Union[Unset, ApiProfileInformation] = UNSET
    point: Union[Unset, ApiOutputUnflashedPropertyResult] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        success = self.api_status

        calculation_id = self.calculation_id
        exception_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exception_info, Unset):
            exception_info = self.exception_info.to_dict()

        profiling: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profiling, Unset):
            profiling = self.profiling.to_dict()

        point: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.point, Unset):
            point = self.point.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if success is not UNSET:
            field_dict["success"] = success
        if calculation_id is not UNSET:
            field_dict["calculationId"] = calculation_id
        if exception_info is not UNSET:
            field_dict["exceptionInfo"] = exception_info
        if profiling is not UNSET:
            field_dict["profiling"] = profiling
        if point is not UNSET:
            field_dict["point"] = point

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = d.pop("success", UNSET)

        calculation_id = d.pop("calculationId", UNSET)

        _exception_info = d.pop("exceptionInfo", UNSET)
        exception_info: Union[Unset, ExceptionInfo]
        if isinstance(_exception_info, Unset):
            exception_info = UNSET
        else:
            exception_info = ExceptionInfo.from_dict(_exception_info)

        _profiling = d.pop("profiling", UNSET)
        profiling: Union[Unset, ApiProfileInformation]
        if isinstance(_profiling, Unset):
            profiling = UNSET
        else:
            profiling = ApiProfileInformation.from_dict(_profiling)

        _point = d.pop("point", UNSET)
        point: Union[Unset, ApiOutputUnflashedPropertyResult]
        if isinstance(_point, Unset):
            point = UNSET
        else:
            point = ApiOutputUnflashedPropertyResult.from_dict(_point)

        unflashed_property_calculation_result = cls(
            success=success,
            calculation_id=calculation_id,
            exception_info=exception_info,
            profiling=profiling,
            point=point,
        )

        return unflashed_property_calculation_result
