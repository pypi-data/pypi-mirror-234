from typing import *

import attr

from ..models.input_data_object_type import InputDataObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InputData")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class InputData:
    """
    Attributes:
        collection_name (str):
        data (List[List[Any]]):
        object_type (Union[Unset, InputDataObjectType]):  Default: InputDataObjectType.INPUTDATA.
    """

    collection_name: str
    data: List[List[Any]]
    object_type: Union[Unset, InputDataObjectType] = InputDataObjectType.INPUTDATA
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        collection_name: str,
        data: List[List[Any]],
        object_type: Union[Unset, InputDataObjectType] = InputDataObjectType.INPUTDATA,
    ):
        """ """

        self.collection_name = collection_name
        self.data = data
        self.object_type = object_type

    def to_dict(self) -> Dict[str, Any]:
        collection_name = self.collection_name
        data = []
        for data_item_data in self.data:
            data_item = data_item_data

            data.append(data_item)

        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_name": collection_name,
                "data": data,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_name = d.pop("collection_name")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = cast(List[Any], data_item_data)

            data.append(data_item)

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, InputDataObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = InputDataObjectType(_object_type)

        input_data = cls(
            collection_name=collection_name,
            data=data,
            object_type=object_type,
        )

        input_data.additional_properties = d
        return input_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
