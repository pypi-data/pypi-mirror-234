from enum import Enum


class IndexObjectType(str, Enum):
    INDEX = "Index"

    def __str__(self) -> str:
        return str(self.value)
