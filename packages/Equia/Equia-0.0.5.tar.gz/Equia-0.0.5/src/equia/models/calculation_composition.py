from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_fluid_distribution_moment import ApiFluidDistributionMoment
from ..models.calculation_block_info import CalculationBlockInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="CalculationComposition")


@attr.s(auto_attribs=True)
class CalculationComposition:
    """Holds composition information for a component"""

    component_id: Union[Unset, str] = UNSET
    component_name: Union[Unset, None, str] = UNSET
    mass: Union[Unset, float] = UNSET
    sorting_order: Union[Unset, int] = UNSET
    moment: Union[Unset, ApiFluidDistributionMoment] = UNSET
    block_infos: Union[Unset, None, List[CalculationBlockInfo]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        component_id = self.component_id
        component_name = self.component_name
        mass = self.mass
        sorting_order = self.sorting_order
        moment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.moment, Unset):
            moment = self.moment.to_dict()

        block_infos: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.block_infos, Unset):
            if self.block_infos is None:
                block_infos = None
            else:
                block_infos = []
                for block_infos_item_data in self.block_infos:
                    block_infos_item = block_infos_item_data.to_dict()

                    block_infos.append(block_infos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if component_id is not UNSET:
            field_dict["componentId"] = component_id
        if component_name is not UNSET:
            field_dict["componentName"] = component_name
        if mass is not UNSET:
            field_dict["mass"] = mass
        if sorting_order is not UNSET:
            field_dict["sortingOrder"] = sorting_order
        if moment is not UNSET:
            field_dict["moment"] = moment
        if block_infos is not UNSET:
            field_dict["blockInfos"] = block_infos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        component_id = d.pop("componentId", UNSET)

        component_name = d.pop("componentName", UNSET)

        mass = d.pop("mass", UNSET)

        sorting_order = d.pop("sortingOrder", UNSET)

        _moment = d.pop("moment", UNSET)
        moment: Union[Unset, ApiFluidDistributionMoment]
        if isinstance(_moment, Unset):
            moment = UNSET
        else:
            moment = ApiFluidDistributionMoment.from_dict(_moment)

        block_infos = []
        _block_infos = d.pop("blockInfos", UNSET)
        for block_infos_item_data in _block_infos or []:
            block_infos_item = CalculationBlockInfo.from_dict(block_infos_item_data)

            block_infos.append(block_infos_item)

        calculation_composition = cls(
            component_id=component_id,
            component_name=component_name,
            mass=mass,
            sorting_order=sorting_order,
            moment=moment,
            block_infos=block_infos,
        )

        return calculation_composition
