from enum import Enum


class QueryParamsObjectType(str, Enum):
    QUERYPARAMS = "QueryParams"

    def __str__(self) -> str:
        return str(self.value)
