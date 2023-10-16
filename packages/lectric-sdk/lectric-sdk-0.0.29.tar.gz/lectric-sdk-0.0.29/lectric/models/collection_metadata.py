from typing import *

import attr

from ..models.collection_metadata_object_type import CollectionMetadataObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionMetadata")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class CollectionMetadata:
    """
    Attributes:
        name (str):
        description (str):
        hash_algo (str):
        etag (str):
        object_type (Union[Unset, CollectionMetadataObjectType]):  Default:
            CollectionMetadataObjectType.COLLECTIONMETADATA.
    """

    name: str
    description: str
    hash_algo: str
    etag: str
    object_type: Union[Unset, CollectionMetadataObjectType] = CollectionMetadataObjectType.COLLECTIONMETADATA
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        name: str,
        description: str,
        hash_algo: str,
        etag: str,
        object_type: Union[Unset, CollectionMetadataObjectType] = CollectionMetadataObjectType.COLLECTIONMETADATA,
    ):
        """ """

        self.name = name
        self.description = description
        self.hash_algo = hash_algo
        self.etag = etag
        self.object_type = object_type

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        hash_algo = self.hash_algo
        etag = self.etag
        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "hash_algo": hash_algo,
                "etag": etag,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        hash_algo = d.pop("hash_algo")

        etag = d.pop("etag")

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, CollectionMetadataObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = CollectionMetadataObjectType(_object_type)

        collection_metadata = cls(
            name=name,
            description=description,
            hash_algo=hash_algo,
            etag=etag,
            object_type=object_type,
        )

        collection_metadata.additional_properties = d
        return collection_metadata

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
