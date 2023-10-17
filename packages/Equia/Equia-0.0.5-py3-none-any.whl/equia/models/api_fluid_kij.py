from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiFluidKij")


@attr.s(auto_attribs=True)
class ApiFluidKij:
    """Set of Kij information"""

    index_i: Union[Unset, int] = UNSET
    index_j: Union[Unset, int] = UNSET
    kija: Union[Unset, float] = UNSET
    kijb: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        index_i = self.index_i
        index_j = self.index_j
        kija = self.kija
        kijb = self.kijb

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if index_i is not UNSET:
            field_dict["indexI"] = index_i
        if index_j is not UNSET:
            field_dict["indexJ"] = index_j
        if kija is not UNSET:
            field_dict["kija"] = kija
        if kijb is not UNSET:
            field_dict["kijb"] = kijb

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        index_i = d.pop("indexI", UNSET)

        index_j = d.pop("indexJ", UNSET)

        kija = d.pop("kija", UNSET)

        kijb = d.pop("kijb", UNSET)

        api_fluid_kij = cls(
            index_i=index_i,
            index_j=index_j,
            kija=kija,
            kijb=kijb,
        )

        return api_fluid_kij
