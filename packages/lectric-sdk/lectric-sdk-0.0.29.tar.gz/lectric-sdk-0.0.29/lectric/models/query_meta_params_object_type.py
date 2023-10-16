from enum import Enum


class QueryMetaParamsObjectType(str, Enum):
    QUERYMETAPARAMS = "QueryMetaParams"

    def __str__(self) -> str:
        return str(self.value)
