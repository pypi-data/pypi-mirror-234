from typing import *

import attr

from ..models.query_params import QueryParams
from ..models.vector_query_spec_object_type import VectorQuerySpecObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="VectorQuerySpec")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class VectorQuerySpec:
    """
    Attributes:
        data (List[List[Any]]):
        collection_name (str):
        search_field (str):
        search_params (QueryParams):
        output_fields (List[str]):
        limit (int):
        object_type (Union[Unset, VectorQuerySpecObjectType]):  Default: VectorQuerySpecObjectType.VECTORQUERYSPEC.
        expr (Union[Unset, str]):
    """

    data: List[List[Any]]
    collection_name: str
    search_field: str
    search_params: QueryParams
    output_fields: List[str]
    limit: int
    object_type: Union[Unset, VectorQuerySpecObjectType] = VectorQuerySpecObjectType.VECTORQUERYSPEC
    expr: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        data: List[List[Any]],
        collection_name: str,
        search_field: str,
        search_params: QueryParams,
        output_fields: List[str],
        limit: int,
        object_type: Union[Unset, VectorQuerySpecObjectType] = VectorQuerySpecObjectType.VECTORQUERYSPEC,
        expr: Union[Unset, str] = UNSET,
    ):
        """ """

        self.data = data
        self.collection_name = collection_name
        self.search_field = search_field
        self.search_params = search_params
        self.output_fields = output_fields
        self.limit = limit
        self.object_type = object_type
        self.expr = expr

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data

            data.append(data_item)

        collection_name = self.collection_name
        search_field = self.search_field
        search_params = self.search_params.to_dict()

        output_fields = self.output_fields

        limit = self.limit
        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        expr = self.expr

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "collection_name": collection_name,
                "search_field": search_field,
                "search_params": search_params,
                "output_fields": output_fields,
                "limit": limit,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if expr is not UNSET:
            field_dict["expr"] = expr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = cast(List[Any], data_item_data)

            data.append(data_item)

        collection_name = d.pop("collection_name")

        search_field = d.pop("search_field")

        search_params = QueryParams.from_dict(d.pop("search_params"))

        output_fields = cast(List[str], d.pop("output_fields"))

        limit = d.pop("limit")

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, VectorQuerySpecObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = VectorQuerySpecObjectType(_object_type)

        expr = unset_if_none(d, "expr")

        vector_query_spec = cls(
            data=data,
            collection_name=collection_name,
            search_field=search_field,
            search_params=search_params,
            output_fields=output_fields,
            limit=limit,
            object_type=object_type,
            expr=expr,
        )

        vector_query_spec.additional_properties = d
        return vector_query_spec

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
