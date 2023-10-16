from io import BytesIO
from typing import *

import attr

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="BodyLookupByFileExactLookupFileCollectionNamePost")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class BodyLookupByFileExactLookupFileCollectionNamePost:
    """
    Attributes:
        file (File):
    """

    file: File
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        file: File,
    ):
        """ """

        self.file = file

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "file": file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        body_lookup_by_file_exact_lookup_file_collection_name_post = cls(
            file=file,
        )

        body_lookup_by_file_exact_lookup_file_collection_name_post.additional_properties = d
        return body_lookup_by_file_exact_lookup_file_collection_name_post

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
