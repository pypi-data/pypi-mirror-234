from typing import *

import attr

from ..models.collection_in_spec_object_type import CollectionInSpecObjectType
from ..models.collection_schema import CollectionSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionInSpec")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class CollectionInSpec:
    """
    Attributes:
        name (str):
        coll_schema (CollectionSchema):
        object_type (Union[Unset, CollectionInSpecObjectType]):  Default: CollectionInSpecObjectType.COLLECTIONINSPEC.
        consistency_level (Union[Unset, str]):  Default: 'Session'.
        approx (Union[Unset, bool]):  Default: True.
    """

    name: str
    coll_schema: CollectionSchema
    object_type: Union[Unset, CollectionInSpecObjectType] = CollectionInSpecObjectType.COLLECTIONINSPEC
    consistency_level: Union[Unset, str] = "Session"
    approx: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        name: str,
        coll_schema: CollectionSchema,
        object_type: Union[Unset, CollectionInSpecObjectType] = CollectionInSpecObjectType.COLLECTIONINSPEC,
        consistency_level: Union[Unset, str] = "Session",
        approx: Union[Unset, bool] = True,
    ):
        """ """

        self.name = name
        self.coll_schema = coll_schema
        self.object_type = object_type
        self.consistency_level = consistency_level
        self.approx = approx

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        coll_schema = self.coll_schema.to_dict()

        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        consistency_level = self.consistency_level
        approx = self.approx

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "coll_schema": coll_schema,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if consistency_level is not UNSET:
            field_dict["consistency_level"] = consistency_level
        if approx is not UNSET:
            field_dict["approx"] = approx

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        coll_schema = CollectionSchema.from_dict(d.pop("coll_schema"))

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, CollectionInSpecObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = CollectionInSpecObjectType(_object_type)

        consistency_level = unset_if_none(d, "consistency_level")

        approx = unset_if_none(d, "approx")

        collection_in_spec = cls(
            name=name,
            coll_schema=coll_schema,
            object_type=object_type,
            consistency_level=consistency_level,
            approx=approx,
        )

        collection_in_spec.additional_properties = d
        return collection_in_spec

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
