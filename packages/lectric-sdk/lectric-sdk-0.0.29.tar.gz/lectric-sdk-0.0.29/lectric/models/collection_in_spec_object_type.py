from enum import Enum


class CollectionInSpecObjectType(str, Enum):
    COLLECTIONINSPEC = "CollectionInSpec"

    def __str__(self) -> str:
        return str(self.value)
