from enum import Enum


class InputDataObjectType(str, Enum):
    INPUTDATA = "InputData"

    def __str__(self) -> str:
        return str(self.value)
