from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.exception_info import ExceptionInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="FluidAddResult")


@attr.s(auto_attribs=True)
class FluidAddResult:
    """Holds result for adding a new fluid to the database"""

    success: Union[Unset, bool] = UNSET
    fluidid: Union[Unset, None, str] = UNSET
    exception_info: Union[Unset, ExceptionInfo] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        success = self.api_status

        fluidid = self.fluidid
        exception_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exception_info, Unset):
            exception_info = self.exception_info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if success is not UNSET:
            field_dict["success"] = success
        if fluidid is not UNSET:
            field_dict["fluidId"] = fluidid
        if exception_info is not UNSET:
            field_dict["exceptionInfo"] = exception_info

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = d.pop("success", UNSET)

        fluidid = d.pop("fluidId", UNSET)

        _exception_info = d.pop("exceptionInfo", UNSET)
        exception_info: Union[Unset, ExceptionInfo]
        if isinstance(_exception_info, Unset):
            exception_info = UNSET
        else:
            exception_info = ExceptionInfo.from_dict(_exception_info)

        new_fluid_result = cls(
            success=success,
            fluidid=fluidid,
            exception_info=exception_info,
        )

        return new_fluid_result
