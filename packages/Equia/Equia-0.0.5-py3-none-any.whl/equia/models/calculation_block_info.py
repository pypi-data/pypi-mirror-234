from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CalculationBlockInfo")


@attr.s(auto_attribs=True)
class CalculationBlockInfo:
    """Information for a copolymer block"""

    commponent_id: Union[Unset, str] = UNSET
    block_name: Union[Unset, None, str] = UNSET
    block_massfraction: Union[Unset, float] = UNSET
    sorting_order: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        commponent_id = self.commponent_id
        block_name = self.block_name
        block_massfraction = self.block_massfraction
        sorting_order = self.sorting_order

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if commponent_id is not UNSET:
            field_dict["commponentId"] = commponent_id
        if block_name is not UNSET:
            field_dict["blockName"] = block_name
        if block_massfraction is not UNSET:
            field_dict["blockMassfraction"] = block_massfraction
        if sorting_order is not UNSET:
            field_dict["sortingOrder"] = sorting_order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        commponent_id = d.pop("commponentId", UNSET)

        block_name = d.pop("blockName", UNSET)

        block_massfraction = d.pop("blockMassfraction", UNSET)

        sorting_order = d.pop("sortingOrder", UNSET)

        calculation_block_info = cls(
            commponent_id=commponent_id,
            block_name=block_name,
            block_massfraction=block_massfraction,
            sorting_order=sorting_order,
        )

        return calculation_block_info
