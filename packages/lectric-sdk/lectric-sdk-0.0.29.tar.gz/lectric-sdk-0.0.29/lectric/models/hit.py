from typing import *

import attr

from ..models.hit_object_type import HitObjectType
from ..models.hit_result import HitResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="Hit")


def unset_if_none(_dict: dict, key: Any) -> Union[Any, Unset]:
    if key not in _dict or _dict[key] is None:
        return UNSET
    return _dict[key]


@attr.s(auto_attribs=True)
class Hit:
    """
    Attributes:
        id (Union[int, str]):
        distance (float):
        result (HitResult):
        object_type (Union[Unset, HitObjectType]):  Default: HitObjectType.HIT.
    """

    id: Union[int, str]
    distance: float
    result: HitResult
    object_type: Union[Unset, HitObjectType] = HitObjectType.HIT
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __init__(
        self,
        id: Union[int, str],
        distance: float,
        result: HitResult,
        object_type: Union[Unset, HitObjectType] = HitObjectType.HIT,
    ):
        """ """

        self.id = id
        self.distance = distance
        self.result = result
        self.object_type = object_type

    def to_dict(self) -> Dict[str, Any]:

        id = self.id

        distance = self.distance
        result = self.result.to_dict()

        object_type: Union[Unset, str] = UNSET
        if not isinstance(self.object_type, Unset):
            object_type = self.object_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "distance": distance,
                "result": result,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_id(data: object) -> Union[int, str]:
            return cast(Union[int, str], data)

        id = _parse_id(d.pop("id"))

        distance = d.pop("distance")

        result = HitResult.from_dict(d.pop("result"))

        _object_type = unset_if_none(d, "object_type")
        object_type: Union[Unset, HitObjectType]
        if isinstance(_object_type, Unset):
            object_type = UNSET
        else:
            object_type = HitObjectType(_object_type)

        hit = cls(
            id=id,
            distance=distance,
            result=result,
            object_type=object_type,
        )

        hit.additional_properties = d
        return hit

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
