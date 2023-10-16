from typing import *

import attr

from ..models.query_meta_params_object_type import QueryMetaParamsObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryMetaParams")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class QueryMetaParams:
    """
    Attributes:
        nprobe (int): Number of units to query. CPU: [1, nlist], GPU: [1, min(2048, nlist)
        object_type (Union[Unset, QueryMetaParamsObjectType]):  Default: QueryMetaParamsObjectType.QUERYMETAPARAMS.
        ef (Union[Unset, int]): Search Scope. Range [top_k, 32768]
        search_k (Union[Unset, int]): The number of nodes to search. -1 means 5% of the whole data. Range {-1} U [top_k,
            n x n_trees]
    """

    nprobe: int
    object_type: Union[Unset, QueryMetaParamsObjectType] = QueryMetaParamsObjectType.QUERYMETAPARAMS
    ef: Union[Unset, int] = UNSET
    search_k: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        nprobe: int,
        object_type: Union[Unset, QueryMetaParamsObjectType] = QueryMetaParamsObjectType.QUERYMETAPARAMS,
        ef: Union[Unset, int] = UNSET,
        search_k: Union[Unset, int] = UNSET,
    ):
        """ """

        self.nprobe = nprobe
        self.object_type = object_type
        self.ef = ef
        self.search_k = search_k

    def to_dict(self) -> Dict[str, Any]:
        nprobe = self.nprobe
        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        ef = self.ef
        search_k = self.search_k

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nprobe": nprobe,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if ef is not UNSET:
            field_dict["ef"] = ef
        if search_k is not UNSET:
            field_dict["search_k"] = search_k

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        nprobe = d.pop("nprobe")

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, QueryMetaParamsObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = QueryMetaParamsObjectType(_object_type)

        ef = unset_if_none(d, "ef")

        search_k = unset_if_none(d, "search_k")

        query_meta_params = cls(
            nprobe=nprobe,
            object_type=object_type,
            ef=ef,
            search_k=search_k,
        )

        query_meta_params.additional_properties = d
        return query_meta_params

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
