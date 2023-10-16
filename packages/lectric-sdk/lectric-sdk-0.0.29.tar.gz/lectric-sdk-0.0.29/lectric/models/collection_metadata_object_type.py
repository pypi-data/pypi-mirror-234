from enum import Enum


class CollectionMetadataObjectType(str, Enum):
    COLLECTIONMETADATA = "CollectionMetadata"

    def __str__(self) -> str:
        return str(self.value)
