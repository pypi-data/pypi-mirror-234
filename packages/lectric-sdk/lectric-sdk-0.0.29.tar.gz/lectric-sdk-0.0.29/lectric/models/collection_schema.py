from typing import *

import attr

from ..models.collection_schema_object_type import CollectionSchemaObjectType
from ..models.field_schema import FieldSchema
from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionSchema")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class CollectionSchema:
    """
    Attributes:
        object_type (Union[Unset, CollectionSchemaObjectType]):  Default: CollectionSchemaObjectType.COLLECTIONSCHEMA.
        fields (Union[Unset, List[FieldSchema]]):
        description (Union[Unset, str]):  Default: ''.
    """

    object_type: Union[Unset, CollectionSchemaObjectType] = CollectionSchemaObjectType.COLLECTIONSCHEMA
    fields: Union[Unset, List[FieldSchema]] = UNSET
    description: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        object_type: Union[Unset, CollectionSchemaObjectType] = CollectionSchemaObjectType.COLLECTIONSCHEMA,
        fields: Union[Unset, List[FieldSchema]] = UNSET,
        description: Union[Unset, str] = "",
    ):
        """ """

        self.object_type = object_type
        self.fields = fields
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        fields: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()

                fields.append(fields_item)

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if fields is not UNSET:
            field_dict["fields"] = fields
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, CollectionSchemaObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = CollectionSchemaObjectType(_object_type)

        fields = []
        _fields = unset_if_none(d, "fields")
        for fields_item_data in _fields or []:
            fields_item = FieldSchema.from_dict(fields_item_data)

            fields.append(fields_item)

        description = unset_if_none(d, "description")

        collection_schema = cls(
            object_type=object_type,
            fields=fields,
            description=description,
        )

        collection_schema.additional_properties = d
        return collection_schema

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
