from enum import Enum


class FieldSchemaObjectType(str, Enum):
    FIELDSCHEMA = "FieldSchema"

    def __str__(self) -> str:
        return str(self.value)
