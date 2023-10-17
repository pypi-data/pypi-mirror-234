from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FluidGetInput")


@attr.s(auto_attribs=True)
class FluidGetInput:
    """Input for request fluid information"""

    access_key: str
    fluidid: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        access_key = self.access_key
        fluidid = self.fluidid

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "accessKey": access_key,
            }
        )
        if fluidid is not UNSET:
            field_dict["fluidId"] = fluidid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        access_key = d.pop("accessKey")

        fluidid = d.pop("fluidId", UNSET)

        request_fluid_input = cls(
            access_key=access_key,
            fluidid=fluidid,
        )

        return request_fluid_input
