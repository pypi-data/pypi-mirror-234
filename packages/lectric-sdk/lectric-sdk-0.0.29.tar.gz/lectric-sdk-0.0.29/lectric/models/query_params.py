from typing import *

import attr

from ..models.query_meta_params import QueryMetaParams
from ..models.query_params_object_type import QueryParamsObjectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="QueryParams")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class QueryParams:
    """
    Attributes:
        metric_type (str): A string corresponding to the Enum: VectorSpace
        params (QueryMetaParams):
        object_type (Union[Unset, QueryParamsObjectType]):  Default: QueryParamsObjectType.QUERYPARAMS.
    """

    metric_type: str
    params: QueryMetaParams
    object_type: Union[Unset, QueryParamsObjectType] = QueryParamsObjectType.QUERYPARAMS
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        metric_type: str,
        params: QueryMetaParams,
        object_type: Union[Unset, QueryParamsObjectType] = QueryParamsObjectType.QUERYPARAMS,
    ):
        """ """

        self.metric_type = metric_type
        self.params = params
        self.object_type = object_type

    def to_dict(self) -> Dict[str, Any]:
        metric_type = self.metric_type
        params = self.params.to_dict()

        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric_type": metric_type,
                "params": params,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metric_type = d.pop("metric_type")

        params = QueryMetaParams.from_dict(d.pop("params"))

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, QueryParamsObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = QueryParamsObjectType(_object_type)

        query_params = cls(
            metric_type=metric_type,
            params=params,
            object_type=object_type,
        )

        query_params.additional_properties = d
        return query_params

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
