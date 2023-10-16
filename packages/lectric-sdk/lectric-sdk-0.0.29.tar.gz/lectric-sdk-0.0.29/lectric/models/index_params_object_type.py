from enum import Enum


class IndexParamsObjectType(str, Enum):
    INDEXPARAMS = "IndexParams"

    def __str__(self) -> str:
        return str(self.value)
