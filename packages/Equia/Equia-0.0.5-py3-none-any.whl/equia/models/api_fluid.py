import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.api_fluid_kij import ApiFluidKij
from ..models.api_fluid_polymer_component import ApiFluidPolymerComponent
from ..models.api_fluid_standard_component import ApiFluidStandardComponent
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiFluid")


@attr.s(auto_attribs=True)
class ApiFluid:
    """Information for a fluid"""

    fluidid: Union[Unset, str] = UNSET
    creation_time: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, None, str] = UNSET
    comment: Union[Unset, None, str] = UNSET
    eos: Union[Unset, str] = UNSET
    property_reference_point: Union[Unset, str] = UNSET
    solvent_cp: Union[Unset, str] = UNSET
    polymer_cp: Union[Unset, str] = UNSET
    standards: Union[Unset, None, List[ApiFluidStandardComponent]] = UNSET
    polymers: Union[Unset, None, List[ApiFluidPolymerComponent]] = UNSET
    kij: Union[Unset, None, List[ApiFluidKij]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fluidid = self.fluidid
        creation_time: Union[Unset, str] = UNSET
        if not isinstance(self.creation_time, Unset):
            creation_time = self.creation_time.isoformat()

        name = self.name
        comment = self.comment
        eos = self.eos

        property_reference_point = self.property_reference_point

        solvent_cp = self.solvent_cp

        polymer_cp = self.polymer_cp

        standards: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.standards, Unset):
            if self.standards is None:
                standards = None
            else:
                standards = []
                for standards_item_data in self.standards:
                    standards_item = standards_item_data.to_dict()

                    standards.append(standards_item)

        polymers: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.polymers, Unset):
            if self.polymers is None:
                polymers = None
            else:
                polymers = []
                for polymers_item_data in self.polymers:
                    polymers_item = polymers_item_data.to_dict()

                    polymers.append(polymers_item)

        kij: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.kij, Unset):
            if self.kij is None:
                kij = None
            else:
                kij = []
                for kij_item_data in self.kij:
                    kij_item = kij_item_data.to_dict()

                    kij.append(kij_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fluidid is not UNSET:
            field_dict["fluidId"] = fluidid
        if creation_time is not UNSET:
            field_dict["creationTime"] = creation_time
        if name is not UNSET:
            field_dict["name"] = name
        if comment is not UNSET:
            field_dict["comment"] = comment
        if eos is not UNSET:
            field_dict["eos"] = eos
        if property_reference_point is not UNSET:
            field_dict["propertyReferencePoint"] = property_reference_point
        if solvent_cp is not UNSET:
            field_dict["solventCp"] = solvent_cp
        if polymer_cp is not UNSET:
            field_dict["polymerCp"] = polymer_cp
        if standards is not UNSET:
            field_dict["standards"] = standards
        if polymers is not UNSET:
            field_dict["polymers"] = polymers
        if kij is not UNSET:
            field_dict["kij"] = kij

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fluidid = d.pop("fluidId", UNSET)

        _creation_time = d.pop("creationTime", UNSET)
        creation_time: Union[Unset, datetime.datetime]
        if isinstance(_creation_time, Unset):
            creation_time = UNSET
        else:
            creation_time = isoparse(_creation_time)

        name = d.pop("name", UNSET)

        comment = d.pop("comment", UNSET)

        eos = d.pop("eos", UNSET)

        property_reference_point = d.pop("propertyReferencePoint", UNSET)

        solvent_cp = d.pop("solventCp", UNSET)

        polymer_cp = d.pop("polymerCp", UNSET)

        standards = []
        _standards = d.pop("standards", UNSET)
        for standards_item_data in _standards or []:
            standards_item = ApiFluidStandardComponent.from_dict(standards_item_data)

            standards.append(standards_item)

        polymers = []
        _polymers = d.pop("polymers", UNSET)
        for polymers_item_data in _polymers or []:
            polymers_item = ApiFluidPolymerComponent.from_dict(polymers_item_data)

            polymers.append(polymers_item)

        kij = []
        _kij = d.pop("kij", UNSET)
        for kij_item_data in _kij or []:
            kij_item = ApiFluidKij.from_dict(kij_item_data)

            kij.append(kij_item)

        api_fluid = cls(
            fluidid=fluidid,
            creation_time=creation_time,
            name=name,
            comment=comment,
            eos=eos,
            property_reference_point=property_reference_point,
            solvent_cp=solvent_cp,
            polymer_cp=polymer_cp,
            standards=standards,
            polymers=polymers,
            kij=kij,
        )

        return api_fluid
