from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiFluidPseudoComponent")


@attr.s(auto_attribs=True)
class ApiFluidPseudoComponent:
    """Information for a pseudo component"""

    sorting_order: Union[Unset, int] = UNSET
    name: Union[Unset, None, str] = UNSET
    melting_temperature: Union[Unset, float] = UNSET
    massfraction: Union[Unset, float] = UNSET
    molar_mass: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sorting_order = self.sorting_order
        name = self.name
        melting_temperature = self.melting_temperature
        massfraction = self.massfraction
        molar_mass = self.molar_mass

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if sorting_order is not UNSET:
            field_dict["sortingOrder"] = sorting_order
        if name is not UNSET:
            field_dict["name"] = name
        if melting_temperature is not UNSET:
            field_dict["meltingTemperature"] = melting_temperature
        if massfraction is not UNSET:
            field_dict["massfraction"] = massfraction
        if molar_mass is not UNSET:
            field_dict["molarMass"] = molar_mass

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sorting_order = d.pop("sortingOrder", UNSET)

        name = d.pop("name", UNSET)

        melting_temperature = d.pop("meltingTemperature", UNSET)

        massfraction = d.pop("massfraction", UNSET)

        molar_mass = d.pop("molarMass", UNSET)

        api_fluid_pseudo_component = cls(
            sorting_order=sorting_order,
            name=name,
            melting_temperature=melting_temperature,
            massfraction=massfraction,
            molar_mass=molar_mass,
        )

        return api_fluid_pseudo_component
