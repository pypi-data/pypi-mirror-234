from enum import Enum


class CollectionSchemaObjectType(str, Enum):
    COLLECTIONSCHEMA = "CollectionSchema"

    def __str__(self) -> str:
        return str(self.value)
