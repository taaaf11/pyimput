from enum import Enum
from typing import Dict, Union, List, Optional


class XInputDeviceMode(Enum):
    ABSOLUTE = 1
    RELATIVE = 2

PropsDict = Dict[str, Union[int, str, List[str]]]
DeviceDataDict = Dict[str, Union[int, str, Dict]]
ButtonsMapDict = Dict[str, str]
OptionalString = Optional[str]
