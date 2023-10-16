from enum import Enum


class CollectionObjectType(str, Enum):
    COLLECTION = "Collection"

    def __str__(self) -> str:
        return str(self.value)
