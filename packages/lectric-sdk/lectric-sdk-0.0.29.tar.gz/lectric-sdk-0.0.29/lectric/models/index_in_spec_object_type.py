from enum import Enum


class IndexInSpecObjectType(str, Enum):
    INDEXINSPEC = "IndexInSpec"

    def __str__(self) -> str:
        return str(self.value)
