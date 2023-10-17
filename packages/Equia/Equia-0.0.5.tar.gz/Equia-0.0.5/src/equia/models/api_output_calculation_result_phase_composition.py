from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_value_composition_array import ApiValueCompositionArray
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPhaseComposition")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPhaseComposition:
    """Holds composition information for a phase"""

    composition_units: Union[Unset, None, str] = UNSET
    molar_mass_units: Union[Unset, None, str] = UNSET
    composition: Union[Unset, ApiValueCompositionArray] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        composition_units = self.composition_units
        molar_mass_units = self.molar_mass_units
        composition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.composition, Unset):
            composition = self.composition.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if composition_units is not UNSET:
            field_dict["compositionUnits"] = composition_units
        if molar_mass_units is not UNSET:
            field_dict["molarMassUnits"] = molar_mass_units
        if composition is not UNSET:
            field_dict["composition"] = composition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        composition_units = d.pop("compositionUnits", UNSET)

        molar_mass_units = d.pop("molarMassUnits", UNSET)

        _composition = d.pop("composition", UNSET)
        composition: Union[Unset, ApiValueCompositionArray]
        if isinstance(_composition, Unset):
            composition = UNSET
        else:
            composition = ApiValueCompositionArray.from_dict(_composition)

        api_output_calculation_result_phase_composition = cls(
            composition_units=composition_units,
            molar_mass_units=molar_mass_units,
            composition=composition,
        )

        return api_output_calculation_result_phase_composition
