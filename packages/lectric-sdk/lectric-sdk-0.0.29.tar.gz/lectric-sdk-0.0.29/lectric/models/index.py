from typing import *

import attr

from ..models.index_object_type import IndexObjectType
from ..models.index_params import IndexParams
from ..types import UNSET, Unset

T = TypeVar("T", bound="Index")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class Index:
    """
    Attributes:
        index_type (str):
        metric_type (str):
        object_type (Union[Unset, IndexObjectType]):  Default: IndexObjectType.INDEX.
        params (Union[Unset, IndexParams]):
    """

    index_type: str
    metric_type: str
    object_type: Union[Unset, IndexObjectType] = IndexObjectType.INDEX
    params: Union[Unset, IndexParams] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        index_type: str,
        metric_type: str,
        object_type: Union[Unset, IndexObjectType] = IndexObjectType.INDEX,
        params: Union[Unset, IndexParams] = UNSET,
    ):
        """ """

        self.index_type = index_type
        self.metric_type = metric_type
        self.object_type = object_type
        self.params = params

    def to_dict(self) -> Dict[str, Any]:
        index_type = self.index_type
        metric_type = self.metric_type
        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index_type": index_type,
                "metric_type": metric_type,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        index_type = d.pop("index_type")

        metric_type = d.pop("metric_type")

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, IndexObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = IndexObjectType(_object_type)

        _params = unset_if_none(d, "params")
        params: Union[Unset, IndexParams]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = IndexParams.from_dict(_params)

        index = cls(
            index_type=index_type,
            metric_type=metric_type,
            object_type=object_type,
            params=params,
        )

        index.additional_properties = d
        return index

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
