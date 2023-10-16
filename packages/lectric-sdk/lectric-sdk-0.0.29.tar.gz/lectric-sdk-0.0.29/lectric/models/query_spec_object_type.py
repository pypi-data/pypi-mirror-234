from enum import Enum


class QuerySpecObjectType(str, Enum):
    QUERYSPEC = "QuerySpec"

    def __str__(self) -> str:
        return str(self.value)
