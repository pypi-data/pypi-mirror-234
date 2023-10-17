from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_output_unflashed_property_result_ideal import ApiOutputUnflashedPropertyResultIdeal
from ..models.api_output_unflashed_property_result_residual import ApiOutputUnflashedPropertyResultResidual
from ..models.api_value_pressure import ApiValuePressure
from ..models.api_value_temperature import ApiValueTemperature
from ..models.api_value_volume import ApiValueVolume
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputUnflashedPropertyResult")


@attr.s(auto_attribs=True)
class ApiOutputUnflashedPropertyResult:
    """Holds result for a point"""

    temperature: Union[Unset, ApiValueTemperature] = UNSET
    pressure: Union[Unset, ApiValuePressure] = UNSET
    volume: Union[Unset, ApiValueVolume] = UNSET
    residual: Union[Unset, ApiOutputUnflashedPropertyResultResidual] = UNSET
    ideal: Union[Unset, ApiOutputUnflashedPropertyResultIdeal] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        temperature: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.temperature, Unset):
            temperature = self.temperature.to_dict()

        pressure: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pressure, Unset):
            pressure = self.pressure.to_dict()

        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        residual: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.residual, Unset):
            residual = self.residual.to_dict()

        ideal: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ideal, Unset):
            ideal = self.ideal.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure
        if volume is not UNSET:
            field_dict["volume"] = volume
        if residual is not UNSET:
            field_dict["residual"] = residual
        if ideal is not UNSET:
            field_dict["ideal"] = ideal

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _temperature = d.pop("temperature", UNSET)
        temperature: Union[Unset, ApiValueTemperature]
        if isinstance(_temperature, Unset):
            temperature = UNSET
        else:
            temperature = ApiValueTemperature.from_dict(_temperature)

        _pressure = d.pop("pressure", UNSET)
        pressure: Union[Unset, ApiValuePressure]
        if isinstance(_pressure, Unset):
            pressure = UNSET
        else:
            pressure = ApiValuePressure.from_dict(_pressure)

        _volume = d.pop("volume", UNSET)
        volume: Union[Unset, ApiValueVolume]
        if isinstance(_volume, Unset):
            volume = UNSET
        else:
            volume = ApiValueVolume.from_dict(_volume)

        _residual = d.pop("residual", UNSET)
        residual: Union[Unset, ApiOutputUnflashedPropertyResultResidual]
        if isinstance(_residual, Unset):
            residual = UNSET
        else:
            residual = ApiOutputUnflashedPropertyResultResidual.from_dict(_residual)

        _ideal = d.pop("ideal", UNSET)
        ideal: Union[Unset, ApiOutputUnflashedPropertyResultIdeal]
        if isinstance(_ideal, Unset):
            ideal = UNSET
        else:
            ideal = ApiOutputUnflashedPropertyResultIdeal.from_dict(_ideal)

        api_output_unflashed_property_result = cls(
            temperature=temperature,
            pressure=pressure,
            volume=volume,
            residual=residual,
            ideal=ideal,
        )

        return api_output_unflashed_property_result
