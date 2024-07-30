from enum import Enum
from typing import Dict, List, Optional, Union


class XInputDeviceCategory(Enum):
    POINTER = "pointer"
    KEYBOARD = "keyboard"
    OTHER = "other"


PropsDict = Dict[str, Dict[str, Union[int, str, List[str]]]]
DeviceDataDict = Dict[str, Union[int, str, Dict]]
ButtonsMapDict = Dict[str, str]
OptionalString = Optional[str]
