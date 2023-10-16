from enum import Enum


class QueryResponseObjectType(str, Enum):
    QUERYRESPONSE = "QueryResponse"

    def __str__(self) -> str:
        return str(self.value)
