from enum import Enum


class HitObjectType(str, Enum):
    HIT = "Hit"

    def __str__(self) -> str:
        return str(self.value)
