from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.api_output_calculation_result_phase_composition import ApiOutputCalculationResultPhaseComposition
from ..models.api_output_calculation_result_phase_polymer_moments import ApiOutputCalculationResultPhasePolymerMoments
from ..models.api_value_compressibility import ApiValueCompressibility
from ..models.api_value_density import ApiValueDensity
from ..models.api_value_enthalpy import ApiValueEnthalpy
from ..models.api_value_entropy import ApiValueEntropy
from ..models.api_value_floating_with_units import ApiValueFloatingWithUnits
from ..models.api_value_mole_percent import ApiValueMolePercent
from ..models.api_value_volume import ApiValueVolume
from ..models.api_value_weight_percent import ApiValueWeightPercent
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiOutputCalculationResultPhase")


@attr.s(auto_attribs=True)
class ApiOutputCalculationResultPhase:
    """Holds all properties for a phase"""

    phase_type: Union[Unset, str] = UNSET
    phase_label: Union[Unset, None, str] = UNSET
    volume: Union[Unset, ApiValueVolume] = UNSET
    density: Union[Unset, ApiValueDensity] = UNSET
    entropy: Union[Unset, ApiValueEntropy] = UNSET
    enthalpy: Union[Unset, ApiValueEnthalpy] = UNSET
    cp: Union[Unset, ApiValueFloatingWithUnits] = UNSET
    cv: Union[Unset, ApiValueFloatingWithUnits] = UNSET
    jt_coefficient: Union[Unset, ApiValueFloatingWithUnits] = UNSET
    speed_of_sound: Union[Unset, ApiValueFloatingWithUnits] = UNSET
    solubility_parameter: Union[Unset, ApiValueFloatingWithUnits] = UNSET
    molecular_weight: Union[Unset, ApiValueFloatingWithUnits] = UNSET
    compressibility: Union[Unset, ApiValueCompressibility] = UNSET
    mole_percent: Union[Unset, ApiValueMolePercent] = UNSET
    weight_percent: Union[Unset, ApiValueWeightPercent] = UNSET
    polymer_moments: Union[Unset,
                           ApiOutputCalculationResultPhasePolymerMoments] = UNSET
    composition: Union[Unset,
                       ApiOutputCalculationResultPhaseComposition] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        phase_type = self.phase_type
        phase_label = self.phase_label
        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        density: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.density, Unset):
            density = self.density.to_dict()

        entropy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entropy, Unset):
            entropy = self.entropy.to_dict()

        enthalpy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.enthalpy, Unset):
            enthalpy = self.enthalpy.to_dict()

        cp: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cp, Unset):
            cp = self.cp.to_dict()

        cv: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cv, Unset):
            cv = self.cv.to_dict()

        jt_coefficient: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.jt_coefficient, Unset):
            jt_coefficient = self.jt_coefficient.to_dict()

        speed_of_sound: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.speed_of_sound, Unset):
            speed_of_sound = self.speed_of_sound.to_dict()

        solubility_parameter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.solubility_parameter, Unset):
            solubility_parameter = self.solubility_parameter.to_dict()

        molecular_weight: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.molecular_weight, Unset):
            molecular_weight = self.molecular_weight.to_dict()

        compressibility: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.compressibility, Unset):
            compressibility = self.compressibility.to_dict()

        mole_percent: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mole_percent, Unset):
            mole_percent = self.mole_percent.to_dict()

        weight_percent: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.weight_percent, Unset):
            weight_percent = self.weight_percent.to_dict()

        polymer_moments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.polymer_moments, Unset):
            polymer_moments = self.polymer_moments.to_dict()

        composition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.composition, Unset):
            composition = self.composition.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if phase_type is not UNSET:
            field_dict["phaseType"] = phase_type
        if phase_label is not UNSET:
            field_dict["phaseLabel"] = phase_label
        if volume is not UNSET:
            field_dict["volume"] = volume
        if density is not UNSET:
            field_dict["density"] = density
        if entropy is not UNSET:
            field_dict["entropy"] = entropy
        if enthalpy is not UNSET:
            field_dict["enthalpy"] = enthalpy
        if cp is not UNSET:
            field_dict["cp"] = cp
        if cv is not UNSET:
            field_dict["cv"] = cv
        if jt_coefficient is not UNSET:
            field_dict["jtcoefficient"] = jt_coefficient
        if speed_of_sound is not UNSET:
            field_dict["speedOfSound"] = speed_of_sound
        if solubility_parameter is not UNSET:
           field_dict["solubilityParameter"] = solubility_parameter
        if molecular_weight is not UNSET:
            field_dict["molecularWeight"] = molecular_weight
        if compressibility is not UNSET:
            field_dict["compressibility"] = compressibility
        if mole_percent is not UNSET:
            field_dict["molePercent"] = mole_percent
        if weight_percent is not UNSET:
            field_dict["weightPercent"] = weight_percent
        if polymer_moments is not UNSET:
            field_dict["polymerMoments"] = polymer_moments
        if composition is not UNSET:
            field_dict["composition"] = composition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        phase_type = d.pop("phaseType", UNSET)

        phase_label = d.pop("phaseLabel", UNSET)

        _volume = d.pop("volume", UNSET)
        volume: Union[Unset, ApiValueVolume]
        if isinstance(_volume, Unset):
            volume = UNSET
        else:
            volume = ApiValueVolume.from_dict(_volume)

        _density = d.pop("density", UNSET)
        density: Union[Unset, ApiValueDensity]
        if isinstance(_density, Unset):
            density = UNSET
        else:
            density = ApiValueDensity.from_dict(_density)

        _entropy = d.pop("entropy", UNSET)
        entropy: Union[Unset, ApiValueEntropy]
        if isinstance(_entropy, Unset):
            entropy = UNSET
        else:
            entropy = ApiValueEntropy.from_dict(_entropy)

        _enthalpy = d.pop("enthalpy", UNSET)
        enthalpy: Union[Unset, ApiValueEnthalpy]
        if isinstance(_enthalpy, Unset):
            enthalpy = UNSET
        else:
            enthalpy = ApiValueEnthalpy.from_dict(_enthalpy)

        _cp = d.pop("cp", UNSET)
        cp: Union[Unset, ApiValueFloatingWithUnits]
        if isinstance(_cp, Unset):
            cp = UNSET
        else:
            cp = ApiValueFloatingWithUnits.from_dict(_cp)

        _cv = d.pop("cv", UNSET)
        cv: Union[Unset, ApiValueFloatingWithUnits]
        if isinstance(_cv, Unset):
            cv = UNSET
        else:
            cv = ApiValueFloatingWithUnits.from_dict(_cv)

        _jt_coefficient = d.pop("jtCoefficient", UNSET)
        jt_coefficient: Union[Unset, ApiValueFloatingWithUnits]
        if isinstance(_jt_coefficient, Unset):
            jt_coefficient = UNSET
        else:
            jt_coefficient = ApiValueFloatingWithUnits.from_dict(_jt_coefficient)

        _speed_of_sound = d.pop("speedOfSound", UNSET)
        speed_of_sound: Union[Unset, ApiValueFloatingWithUnits]
        if isinstance(_speed_of_sound, Unset):
            speed_of_sound = UNSET
        else:
            speed_of_sound = ApiValueFloatingWithUnits.from_dict(
                _speed_of_sound)

        _solubility_parameter = d.pop("solubilityParameter", UNSET)
        solubility_parameter: Union[Unset, ApiValueFloatingWithUnits]
        if isinstance(_solubility_parameter, Unset):
            solubility_parameter = UNSET
        else:
            solubility_parameter = ApiValueFloatingWithUnits.from_dict(_solubility_parameter)

        _molecular_weight = d.pop("molecularWeight", UNSET)
        molecular_weight: Union[Unset, ApiValueFloatingWithUnits]
        if isinstance(_molecular_weight, Unset):
            molecular_weight = UNSET
        else:
            molecular_weight = ApiValueFloatingWithUnits.from_dict(
                _molecular_weight)

        _compressibility = d.pop("compressibility", UNSET)
        compressibility: Union[Unset, ApiValueCompressibility]
        if isinstance(_compressibility, Unset):
            compressibility = UNSET
        else:
            compressibility = ApiValueCompressibility.from_dict(
                _compressibility)

        _mole_percent = d.pop("molePercent", UNSET)
        mole_percent: Union[Unset, ApiValueMolePercent]
        if isinstance(_mole_percent, Unset):
            mole_percent = UNSET
        else:
            mole_percent = ApiValueMolePercent.from_dict(_mole_percent)

        _weight_percent = d.pop("weightPercent", UNSET)
        weight_percent: Union[Unset, ApiValueWeightPercent]
        if isinstance(_weight_percent, Unset):
            weight_percent = UNSET
        else:
            weight_percent = ApiValueWeightPercent.from_dict(_weight_percent)

        _polymer_moments = d.pop("polymerMoments", UNSET)
        polymer_moments: Union[Unset,
                               ApiOutputCalculationResultPhasePolymerMoments]
        if isinstance(_polymer_moments, Unset):
            polymer_moments = UNSET
        else:
            polymer_moments = ApiOutputCalculationResultPhasePolymerMoments.from_dict(
                _polymer_moments)

        _composition = d.pop("composition", UNSET)
        composition: Union[Unset, ApiOutputCalculationResultPhaseComposition]
        if isinstance(_composition, Unset):
            composition = UNSET
        else:
            composition = ApiOutputCalculationResultPhaseComposition.from_dict(
                _composition)

        api_output_calculation_result_phase = cls(
            phase_type=phase_type,
            phase_label=phase_label,
            volume=volume,
            density=density,
            entropy=entropy,
            enthalpy=enthalpy,
            cp=cp,
            cv=cv,
            jt_coefficient=jt_coefficient,
            speed_of_sound=speed_of_sound,
            solubility_parameter=solubility_parameter,
            molecular_weight=molecular_weight,
            compressibility=compressibility,
            mole_percent=mole_percent,
            weight_percent=weight_percent,
            polymer_moments=polymer_moments,
            composition=composition,
        )

        return api_output_calculation_result_phase
