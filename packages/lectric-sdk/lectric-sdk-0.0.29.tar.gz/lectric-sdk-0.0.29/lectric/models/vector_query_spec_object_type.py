from enum import Enum


class VectorQuerySpecObjectType(str, Enum):
    VECTORQUERYSPEC = "VectorQuerySpec"

    def __str__(self) -> str:
        return str(self.value)
