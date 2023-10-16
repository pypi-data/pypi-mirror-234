from typing import *

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaInfoExactSchemaInfoGetResponseSchemaInfoExactSchemaInfoGet")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class SchemaInfoExactSchemaInfoGetResponseSchemaInfoExactSchemaInfoGet:
    """ """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
    ):
        """ """

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schema_info_exact_schema_info_get_response_schema_info_exact_schema_info_get = cls()

        schema_info_exact_schema_info_get_response_schema_info_exact_schema_info_get.additional_properties = d
        return schema_info_exact_schema_info_get_response_schema_info_exact_schema_info_get

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
