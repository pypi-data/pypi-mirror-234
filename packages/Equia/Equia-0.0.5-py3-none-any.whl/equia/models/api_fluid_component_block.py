from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiFluidComponentBlock")


@attr.s(auto_attribs=True)
class ApiFluidComponentBlock:
    """Values for a component block"""

    sorting_order: Union[Unset, int] = UNSET
    block_massfraction: Union[Unset, float] = UNSET
    block_name: Union[Unset, None, str] = UNSET
    monomer_name: Union[Unset, None, str] = UNSET
    monomer_molar_mass: Union[Unset, float] = UNSET
    pc_saft_epsilon: Union[Unset, float] = UNSET
    pc_saft_sigma_0: Union[Unset, float] = UNSET
    pc_saft_sigma_1: Union[Unset, float] = UNSET
    pc_saft_sigma_2: Union[Unset, float] = UNSET
    pc_saft_sigma_3: Union[Unset, float] = UNSET
    pc_saft_sigma_4: Union[Unset, float] = UNSET
    pc_saftdm: Union[Unset, float] = UNSET
    pc_saft_ab_active: Union[Unset, bool] = UNSET
    pc_saft_ab_kappa: Union[Unset, float] = UNSET
    pc_saft_ab_epsilon: Union[Unset, float] = UNSET
    pc_saft_ab_scheme: Union[Unset, str] = UNSET
    pc_saft_polar_active: Union[Unset, bool] = UNSET
    pc_saft_polarx: Union[Unset, float] = UNSET
    pc_saft_polar_d: Union[Unset, float] = UNSET
    sle_c: Union[Unset, float] = UNSET
    sle_hu: Union[Unset, float] = UNSET
    sle_density_amorphous: Union[Unset, float] = UNSET
    sle_density_crystalline: Union[Unset, float] = UNSET
    sle_tss: Union[Unset, float] = UNSET
    sle_hss: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c0: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c1: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c2: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c3: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c4: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c5: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c6: Union[Unset, float] = UNSET
    pc_saft_cp_ig_poly_c7: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c0: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c1: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c2: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c3: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c4: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c5: Union[Unset, float] = UNSET
    pc_saft_cp_ig_dippr_c6: Union[Unset, float] = UNSET
    ideal_gas_enthalpy_of_formation: Union[Unset, float] = UNSET
    ideal_gas_gibbs_energy_of_formation: Union[Unset, float] = UNSET
    ideal_gas_absolute_entropy: Union[Unset, float] = UNSET
    standard_state_enthalpy_of_formation: Union[Unset, float] = UNSET
    standard_state_gibbs_energy_of_formation: Union[Unset, float] = UNSET
    standard_state_absolute_entropy: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sorting_order = self.sorting_order
        block_massfraction = self.block_massfraction
        block_name = self.block_name
        monomer_name = self.monomer_name
        monomer_molar_mass = self.monomer_molar_mass
        pc_saft_epsilon = self.pc_saft_epsilon
        pc_saft_sigma_0 = self.pc_saft_sigma_0
        pc_saft_sigma_1 = self.pc_saft_sigma_1
        pc_saft_sigma_2 = self.pc_saft_sigma_2
        pc_saft_sigma_3 = self.pc_saft_sigma_3
        pc_saft_sigma_4 = self.pc_saft_sigma_4
        pc_saftdm = self.pc_saftdm
        pc_saft_ab_active = self.pc_saft_ab_active
        pc_saft_ab_kappa = self.pc_saft_ab_kappa
        pc_saft_ab_epsilon = self.pc_saft_ab_epsilon
        pc_saft_ab_scheme = self.pc_saft_ab_scheme

        pc_saft_polar_active = self.pc_saft_polar_active
        pc_saft_polarx = self.pc_saft_polarx
        pc_saft_polar_d = self.pc_saft_polar_d
        sle_c = self.sle_c
        sle_hu = self.sle_hu
        sle_density_amorphous = self.sle_density_amorphous
        sle_density_crystalline = self.sle_density_crystalline
        sle_tss = self.sle_tss
        sle_hss = self.sle_hss
        pc_saft_cp_ig_poly_c0 = self.pc_saft_cp_ig_poly_c0
        pc_saft_cp_ig_poly_c1 = self.pc_saft_cp_ig_poly_c1
        pc_saft_cp_ig_poly_c2 = self.pc_saft_cp_ig_poly_c2
        pc_saft_cp_ig_poly_c3 = self.pc_saft_cp_ig_poly_c3
        pc_saft_cp_ig_poly_c4 = self.pc_saft_cp_ig_poly_c4
        pc_saft_cp_ig_poly_c5 = self.pc_saft_cp_ig_poly_c5
        pc_saft_cp_ig_poly_c6 = self.pc_saft_cp_ig_poly_c6
        pc_saft_cp_ig_poly_c7 = self.pc_saft_cp_ig_poly_c7
        pc_saft_cp_ig_dippr_c0 = self.pc_saft_cp_ig_dippr_c0
        pc_saft_cp_ig_dippr_c1 = self.pc_saft_cp_ig_dippr_c1
        pc_saft_cp_ig_dippr_c2 = self.pc_saft_cp_ig_dippr_c2
        pc_saft_cp_ig_dippr_c3 = self.pc_saft_cp_ig_dippr_c3
        pc_saft_cp_ig_dippr_c4 = self.pc_saft_cp_ig_dippr_c4
        pc_saft_cp_ig_dippr_c5 = self.pc_saft_cp_ig_dippr_c5
        pc_saft_cp_ig_dippr_c6 = self.pc_saft_cp_ig_dippr_c6
        ideal_gas_enthalpy_of_formation = self.ideal_gas_enthalpy_of_formation
        ideal_gas_gibbs_energy_of_formation = self.ideal_gas_gibbs_energy_of_formation
        ideal_gas_absolute_entropy = self.ideal_gas_absolute_entropy
        standard_state_enthalpy_of_formation = self.standard_state_enthalpy_of_formation
        standard_state_gibbs_energy_of_formation = self.standard_state_gibbs_energy_of_formation
        standard_state_absolute_entropy = self.standard_state_absolute_entropy

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if sorting_order is not UNSET:
            field_dict["sortingOrder"] = sorting_order
        if block_massfraction is not UNSET:
            field_dict["blockMassfraction"] = block_massfraction
        if block_name is not UNSET:
            field_dict["blockName"] = block_name
        if monomer_name is not UNSET:
            field_dict["monomerName"] = monomer_name
        if monomer_molar_mass is not UNSET:
            field_dict["monomerMolarMass"] = monomer_molar_mass
        if pc_saft_epsilon is not UNSET:
            field_dict["pcSaftEpsilon"] = pc_saft_epsilon
        if pc_saft_sigma_0 is not UNSET:
            field_dict["pcSaftSigma0"] = pc_saft_sigma_0
        if pc_saft_sigma_1 is not UNSET:
            field_dict["pcSaftSigma1"] = pc_saft_sigma_1
        if pc_saft_sigma_2 is not UNSET:
            field_dict["pcSaftSigma2"] = pc_saft_sigma_2
        if pc_saft_sigma_3 is not UNSET:
            field_dict["pcSaftSigma3"] = pc_saft_sigma_3
        if pc_saft_sigma_4 is not UNSET:
            field_dict["pcSaftSigma4"] = pc_saft_sigma_4
        if pc_saftdm is not UNSET:
            field_dict["pcSaftdm"] = pc_saftdm
        if pc_saft_ab_active is not UNSET:
            field_dict["pcSaftAbActive"] = pc_saft_ab_active
        if pc_saft_ab_kappa is not UNSET:
            field_dict["pcSaftAbKappa"] = pc_saft_ab_kappa
        if pc_saft_ab_epsilon is not UNSET:
            field_dict["pcSaftAbEpsilon"] = pc_saft_ab_epsilon
        if pc_saft_ab_scheme is not UNSET:
            field_dict["pcSaftAbScheme"] = pc_saft_ab_scheme
        if pc_saft_polar_active is not UNSET:
            field_dict["pcSaftPolarActive"] = pc_saft_polar_active
        if pc_saft_polarx is not UNSET:
            field_dict["pcSaftPolarx"] = pc_saft_polarx
        if pc_saft_polar_d is not UNSET:
            field_dict["pcSaftPolarD"] = pc_saft_polar_d
        if sle_c is not UNSET:
            field_dict["sleC"] = sle_c
        if sle_hu is not UNSET:
            field_dict["sleHu"] = sle_hu
        if sle_density_amorphous is not UNSET:
            field_dict["sleDensityAmorphous"] = sle_density_amorphous
        if sle_density_crystalline is not UNSET:
            field_dict["sleDensityCrystalline"] = sle_density_crystalline
        if sle_tss is not UNSET:
            field_dict["sleTss"] = sle_tss
        if sle_hss is not UNSET:
            field_dict["sleHss"] = sle_hss
        if pc_saft_cp_ig_poly_c0 is not UNSET:
            field_dict["pcSaftCpIgPolyC0"] = pc_saft_cp_ig_poly_c0
        if pc_saft_cp_ig_poly_c1 is not UNSET:
            field_dict["pcSaftCpIgPolyC1"] = pc_saft_cp_ig_poly_c1
        if pc_saft_cp_ig_poly_c2 is not UNSET:
            field_dict["pcSaftCpIgPolyC2"] = pc_saft_cp_ig_poly_c2
        if pc_saft_cp_ig_poly_c3 is not UNSET:
            field_dict["pcSaftCpIgPolyC3"] = pc_saft_cp_ig_poly_c3
        if pc_saft_cp_ig_poly_c4 is not UNSET:
            field_dict["pcSaftCpIgPolyC4"] = pc_saft_cp_ig_poly_c4
        if pc_saft_cp_ig_poly_c5 is not UNSET:
            field_dict["pcSaftCpIgPolyC5"] = pc_saft_cp_ig_poly_c5
        if pc_saft_cp_ig_poly_c6 is not UNSET:
            field_dict["pcSaftCpIgPolyC6"] = pc_saft_cp_ig_poly_c6
        if pc_saft_cp_ig_poly_c7 is not UNSET:
            field_dict["pcSaftCpIgPolyC7"] = pc_saft_cp_ig_poly_c7
        if pc_saft_cp_ig_dippr_c0 is not UNSET:
            field_dict["pcSaftCpIgDipprC0"] = pc_saft_cp_ig_dippr_c0
        if pc_saft_cp_ig_dippr_c1 is not UNSET:
            field_dict["pcSaftCpIgDipprC1"] = pc_saft_cp_ig_dippr_c1
        if pc_saft_cp_ig_dippr_c2 is not UNSET:
            field_dict["pcSaftCpIgDipprC2"] = pc_saft_cp_ig_dippr_c2
        if pc_saft_cp_ig_dippr_c3 is not UNSET:
            field_dict["pcSaftCpIgDipprC3"] = pc_saft_cp_ig_dippr_c3
        if pc_saft_cp_ig_dippr_c4 is not UNSET:
            field_dict["pcSaftCpIgDipprC4"] = pc_saft_cp_ig_dippr_c4
        if pc_saft_cp_ig_dippr_c5 is not UNSET:
            field_dict["pcSaftCpIgDipprC5"] = pc_saft_cp_ig_dippr_c5
        if pc_saft_cp_ig_dippr_c6 is not UNSET:
            field_dict["pcSaftCpIgDipprC6"] = pc_saft_cp_ig_dippr_c6
        if ideal_gas_enthalpy_of_formation is not UNSET:
            field_dict["idealGasEnthalpyOfFormation"] = ideal_gas_enthalpy_of_formation
        if ideal_gas_gibbs_energy_of_formation is not UNSET:
            field_dict["idealGasGibbsEnergyOfFormation"] = ideal_gas_gibbs_energy_of_formation
        if ideal_gas_absolute_entropy is not UNSET:
            field_dict["idealGasAbsoluteEntropy"] = ideal_gas_absolute_entropy
        if standard_state_enthalpy_of_formation is not UNSET:
            field_dict["standardStateEnthalpyOfFormation"] = standard_state_enthalpy_of_formation
        if standard_state_gibbs_energy_of_formation is not UNSET:
            field_dict["standardStateGibbsEnergyOfFormation"] = standard_state_gibbs_energy_of_formation
        if standard_state_absolute_entropy is not UNSET:
            field_dict["standardStateAbsoluteEntropy"] = standard_state_absolute_entropy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sorting_order = d.pop("sortingOrder", UNSET)

        block_massfraction = d.pop("blockMassfraction", UNSET)

        block_name = d.pop("blockName", UNSET)

        monomer_name = d.pop("monomerName", UNSET)

        monomer_molar_mass = d.pop("monomerMolarMass", UNSET)

        pc_saft_epsilon = d.pop("pcSaftEpsilon", UNSET)

        pc_saft_sigma_0 = d.pop("pcSaftSigma0", UNSET)

        pc_saft_sigma_1 = d.pop("pcSaftSigma1", UNSET)

        pc_saft_sigma_2 = d.pop("pcSaftSigma2", UNSET)

        pc_saft_sigma_3 = d.pop("pcSaftSigma3", UNSET)

        pc_saft_sigma_4 = d.pop("pcSaftSigma4", UNSET)

        pc_saftdm = d.pop("pcSaftdm", UNSET)

        pc_saft_ab_active = d.pop("pcSaftAbActive", UNSET)

        pc_saft_ab_kappa = d.pop("pcSaftAbKappa", UNSET)

        pc_saft_ab_epsilon = d.pop("pcSaftAbEpsilon", UNSET)

        pc_saft_ab_scheme = d.pop("pcSaftAbScheme", UNSET)

        pc_saft_polar_active = d.pop("pcSaftPolarActive", UNSET)

        pc_saft_polarx = d.pop("pcSaftPolarx", UNSET)

        pc_saft_polar_d = d.pop("pcSaftPolarD", UNSET)

        sle_c = d.pop("sleC", UNSET)

        sle_hu = d.pop("sleHu", UNSET)

        sle_density_amorphous = d.pop("sleDensityAmorphous", UNSET)

        sle_density_crystalline = d.pop("sleDensityCrystalline", UNSET)

        sle_tss = d.pop("sleTss", UNSET)

        sle_hss = d.pop("sleHss", UNSET)

        pc_saft_cp_ig_poly_c0 = d.pop("pcSaftCpIgPolyC0", UNSET)

        pc_saft_cp_ig_poly_c1 = d.pop("pcSaftCpIgPolyC1", UNSET)

        pc_saft_cp_ig_poly_c2 = d.pop("pcSaftCpIgPolyC2", UNSET)

        pc_saft_cp_ig_poly_c3 = d.pop("pcSaftCpIgPolyC3", UNSET)

        pc_saft_cp_ig_poly_c4 = d.pop("pcSaftCpIgPolyC4", UNSET)

        pc_saft_cp_ig_poly_c5 = d.pop("pcSaftCpIgPolyC5", UNSET)

        pc_saft_cp_ig_poly_c6 = d.pop("pcSaftCpIgPolyC6", UNSET)

        pc_saft_cp_ig_poly_c7 = d.pop("pcSaftCpIgPolyC7", UNSET)

        pc_saft_cp_ig_dippr_c0 = d.pop("pcSaftCpIgDipprC0", UNSET)

        pc_saft_cp_ig_dippr_c1 = d.pop("pcSaftCpIgDipprC1", UNSET)

        pc_saft_cp_ig_dippr_c2 = d.pop("pcSaftCpIgDipprC2", UNSET)

        pc_saft_cp_ig_dippr_c3 = d.pop("pcSaftCpIgDipprC3", UNSET)

        pc_saft_cp_ig_dippr_c4 = d.pop("pcSaftCpIgDipprC4", UNSET)

        pc_saft_cp_ig_dippr_c5 = d.pop("pcSaftCpIgDipprC5", UNSET)

        pc_saft_cp_ig_dippr_c6 = d.pop("pcSaftCpIgDipprC6", UNSET)

        ideal_gas_enthalpy_of_formation = d.pop("idealGasEnthalpyOfFormation", UNSET)

        ideal_gas_gibbs_energy_of_formation = d.pop("idealGasGibbsEnergyOfFormation", UNSET)

        ideal_gas_absolute_entropy = d.pop("idealGasAbsoluteEntropy", UNSET)

        standard_state_enthalpy_of_formation = d.pop("standardStateEnthalpyOfFormation", UNSET)

        standard_state_gibbs_energy_of_formation = d.pop("standardStateGibbsEnergyOfFormation", UNSET)

        standard_state_absolute_entropy = d.pop("standardStateAbsoluteEntropy", UNSET)

        api_fluid_component_block = cls(
            sorting_order=sorting_order,
            block_massfraction=block_massfraction,
            block_name=block_name,
            monomer_name=monomer_name,
            monomer_molar_mass=monomer_molar_mass,
            pc_saft_epsilon=pc_saft_epsilon,
            pc_saft_sigma_0=pc_saft_sigma_0,
            pc_saft_sigma_1=pc_saft_sigma_1,
            pc_saft_sigma_2=pc_saft_sigma_2,
            pc_saft_sigma_3=pc_saft_sigma_3,
            pc_saft_sigma_4=pc_saft_sigma_4,
            pc_saftdm=pc_saftdm,
            pc_saft_ab_active=pc_saft_ab_active,
            pc_saft_ab_kappa=pc_saft_ab_kappa,
            pc_saft_ab_epsilon=pc_saft_ab_epsilon,
            pc_saft_ab_scheme=pc_saft_ab_scheme,
            pc_saft_polar_active=pc_saft_polar_active,
            pc_saft_polarx=pc_saft_polarx,
            pc_saft_polar_d=pc_saft_polar_d,
            sle_c=sle_c,
            sle_hu=sle_hu,
            sle_density_amorphous=sle_density_amorphous,
            sle_density_crystalline=sle_density_crystalline,
            sle_tss=sle_tss,
            sle_hss=sle_hss,
            pc_saft_cp_ig_poly_c0=pc_saft_cp_ig_poly_c0,
            pc_saft_cp_ig_poly_c1=pc_saft_cp_ig_poly_c1,
            pc_saft_cp_ig_poly_c2=pc_saft_cp_ig_poly_c2,
            pc_saft_cp_ig_poly_c3=pc_saft_cp_ig_poly_c3,
            pc_saft_cp_ig_poly_c4=pc_saft_cp_ig_poly_c4,
            pc_saft_cp_ig_poly_c5=pc_saft_cp_ig_poly_c5,
            pc_saft_cp_ig_poly_c6=pc_saft_cp_ig_poly_c6,
            pc_saft_cp_ig_poly_c7=pc_saft_cp_ig_poly_c7,
            pc_saft_cp_ig_dippr_c0=pc_saft_cp_ig_dippr_c0,
            pc_saft_cp_ig_dippr_c1=pc_saft_cp_ig_dippr_c1,
            pc_saft_cp_ig_dippr_c2=pc_saft_cp_ig_dippr_c2,
            pc_saft_cp_ig_dippr_c3=pc_saft_cp_ig_dippr_c3,
            pc_saft_cp_ig_dippr_c4=pc_saft_cp_ig_dippr_c4,
            pc_saft_cp_ig_dippr_c5=pc_saft_cp_ig_dippr_c5,
            pc_saft_cp_ig_dippr_c6=pc_saft_cp_ig_dippr_c6,
            ideal_gas_enthalpy_of_formation=ideal_gas_enthalpy_of_formation,
            ideal_gas_gibbs_energy_of_formation=ideal_gas_gibbs_energy_of_formation,
            ideal_gas_absolute_entropy=ideal_gas_absolute_entropy,
            standard_state_enthalpy_of_formation=standard_state_enthalpy_of_formation,
            standard_state_gibbs_energy_of_formation=standard_state_gibbs_energy_of_formation,
            standard_state_absolute_entropy=standard_state_absolute_entropy,
        )

        return api_fluid_component_block
