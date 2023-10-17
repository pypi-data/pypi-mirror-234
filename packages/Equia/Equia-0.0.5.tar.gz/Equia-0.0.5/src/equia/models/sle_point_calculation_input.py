from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.calculation_composition import CalculationComposition
from ..models.api_fluid import ApiFluid
from ..types import UNSET, Unset

T = TypeVar("T", bound="SlePointCalculationInput")


@attr.s(auto_attribs=True)
class SlePointCalculationInput:
    """Input for SLE point calculation"""

    access_key: str
    components: List[CalculationComposition]
    pointtype: str # Type of calculation. Allowed values are: Fixed Pressure, Fixed Temperature/Pressure
    units: str
    fluidid: Union[Unset, str] = UNSET #Id of fluid on webserver. Must be defined if no fluid given in fluid argument
    fluid: Union[Unset, ApiFluid] = UNSET #Fluid information
    temperature: Union[Unset, float] = UNSET
    pressure: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        access_key = self.access_key
        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()

            components.append(components_item)

        pointtype = self.pointtype

        units = self.units

        temperature = self.temperature
        pressure = self.pressure

        fluidid: Union[Unset, str] = UNSET
        if not isinstance(self.fluidid, Unset):
            fluid = self.fluidid

        fluid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fluid, Unset):
            fluid = self.fluid.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "accessKey": access_key,
                "components": components,
                "pointType": pointtype,
            }
        )
        if units is not UNSET:
            field_dict["units"] = units
        if fluidid is not UNSET:
            field_dict["fluidId"] = fluidid
        if fluid is not UNSET:
            field_dict["fluid"] = fluid
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if pressure is not UNSET:
            field_dict["pressure"] = pressure

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        access_key = d.pop("accessKey")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = CalculationComposition.from_dict(components_item_data)

            components.append(components_item)

        _fluidid = d.pop("fluidId", UNSET)
        fluidid: Union[Unset, str]
        if isinstance(_fluidid, Unset):
            fluidid = UNSET
        else:
            fluidid = _fluidid

        _fluid = d.pop("fluid", UNSET)
        fluid: Union[Unset, ApiFluid]
        if isinstance(_fluid, Unset):
            fluid = UNSET
        else:
            fluid = ApiFluid.from_dict(_fluid)
        pointtype = d.pop("pointType")

        units = d.pop("units", UNSET)

        temperature = d.pop("temperature", UNSET)

        pressure = d.pop("pressure", UNSET)

        sle_point_calculation_input = cls(
            access_key=access_key,
            components=components,
            fluidid=fluidid,
            fluid=fluid,
            pointtype=pointtype,
            units=units,
            temperature=temperature,
            pressure=pressure,
        )

        return sle_point_calculation_input
