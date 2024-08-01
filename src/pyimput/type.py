from enum import Enum
from typing import Dict, List, Optional, Union


class XInputDeviceMode(Enum):
    ABSOLUTE = 1
    RELATIVE = 2


class XInputDeviceCategory(Enum):
    POINTER = "pointer"
    KEYBOARD = "keyboard"
    OTHER = "other"


class GetByNameMethod(Enum):
    CONTAINS = "contains"
    EQ = "eq"


PropsDict = Dict[str, Dict[str, Union[int, str, List[str]]]]
DeviceDataDict = Dict[str, Union[int, str, Dict]]
ButtonsMapDict = Dict[str, str]
OptionalString = Optional[str]
