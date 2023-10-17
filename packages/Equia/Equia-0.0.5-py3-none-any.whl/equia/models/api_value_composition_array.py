from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.api_value_component_composition import ApiValueComponentComposition
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiValueCompositionArray")


@attr.s(auto_attribs=True)
class ApiValueCompositionArray:
    """Holds compositioninfo"""

    components: Union[Unset, None, List[ApiValueComponentComposition]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        components: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            if self.components is None:
                components = None
            else:
                components = []
                for components_item_data in self.components:
                    components_item = components_item_data.to_dict()

                    components.append(components_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if components is not UNSET:
            field_dict["components"] = components

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = ApiValueComponentComposition.from_dict(components_item_data)

            components.append(components_item)

        api_value_composition_array = cls(
            components=components,
        )

        return api_value_composition_array
