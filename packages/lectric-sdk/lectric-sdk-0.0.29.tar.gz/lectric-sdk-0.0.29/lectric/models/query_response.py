from typing import *

import attr

from ..models.hit import Hit
from ..models.query_response_object_type import QueryResponseObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryResponse")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class QueryResponse:
    """
    Attributes:
        collection_name (str):
        hits (List[List[Hit]]):
        query_latency (float):
        total_latency (float):
        object_type (Union[Unset, QueryResponseObjectType]):  Default: QueryResponseObjectType.QUERYRESPONSE.
    """

    collection_name: str
    hits: List[List[Hit]]
    query_latency: float
    total_latency: float
    object_type: Union[Unset, QueryResponseObjectType] = QueryResponseObjectType.QUERYRESPONSE
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        collection_name: str,
        hits: List[List[Hit]],
        query_latency: float,
        total_latency: float,
        object_type: Union[Unset, QueryResponseObjectType] = QueryResponseObjectType.QUERYRESPONSE,
    ):
        """ """

        self.collection_name = collection_name
        self.hits = hits
        self.query_latency = query_latency
        self.total_latency = total_latency
        self.object_type = object_type

    def to_dict(self) -> Dict[str, Any]:
        collection_name = self.collection_name
        hits = []
        for hits_item_data in self.hits:
            hits_item = []
            for hits_item_item_data in hits_item_data:
                hits_item_item = hits_item_item_data.to_dict()

                hits_item.append(hits_item_item)

            hits.append(hits_item)

        query_latency = self.query_latency
        total_latency = self.total_latency
        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_name": collection_name,
                "hits": hits,
                "query_latency": query_latency,
                "total_latency": total_latency,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_name = d.pop("collection_name")

        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = []
            _hits_item = hits_item_data
            for hits_item_item_data in _hits_item:
                hits_item_item = Hit.from_dict(hits_item_item_data)

                hits_item.append(hits_item_item)

            hits.append(hits_item)

        query_latency = d.pop("query_latency")

        total_latency = d.pop("total_latency")

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, QueryResponseObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = QueryResponseObjectType(_object_type)

        query_response = cls(
            collection_name=collection_name,
            hits=hits,
            query_latency=query_latency,
            total_latency=total_latency,
            object_type=object_type,
        )

        query_response.additional_properties = d
        return query_response

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
