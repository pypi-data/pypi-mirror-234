from typing import *

import attr

from ..models.index import Index
from ..models.index_in_spec_object_type import IndexInSpecObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexInSpec")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class IndexInSpec:
    """
    Attributes:
        collection_name (str):
        field_name (str):
        index (Index):
        object_type (Union[Unset, IndexInSpecObjectType]):  Default: IndexInSpecObjectType.INDEXINSPEC.
    """

    collection_name: str
    field_name: str
    index: Index
    object_type: Union[Unset, IndexInSpecObjectType] = IndexInSpecObjectType.INDEXINSPEC
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        collection_name: str,
        field_name: str,
        index: Index,
        object_type: Union[Unset, IndexInSpecObjectType] = IndexInSpecObjectType.INDEXINSPEC,
    ):
        """ """

        self.collection_name = collection_name
        self.field_name = field_name
        self.index = index
        self.object_type = object_type

    def to_dict(self) -> Dict[str, Any]:
        collection_name = self.collection_name
        field_name = self.field_name
        index = self.index.to_dict()

        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_name": collection_name,
                "field_name": field_name,
                "index": index,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_name = d.pop("collection_name")

        field_name = d.pop("field_name")

        index = Index.from_dict(d.pop("index"))

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, IndexInSpecObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = IndexInSpecObjectType(_object_type)

        index_in_spec = cls(
            collection_name=collection_name,
            field_name=field_name,
            index=index,
            object_type=object_type,
        )

        index_in_spec.additional_properties = d
        return index_in_spec

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
