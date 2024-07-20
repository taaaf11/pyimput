import subprocess
from typing import List, Sequence, Union

from type import XInputDeviceMode

from .properties import Properties

# fix circular import
# from ..utils import get_command_output, run_command


# fix circular import
def get_command_output(command: List[str]):
    return subprocess.run(command, capture_output=True).stdout


run_command = subprocess.run


class XInputDevice:
    def __init__(self, device_data: dict, debug=False):
        self.__id = device_data["id"]
        self.__name = device_data["device_name"]
        self.__master_id = device_data["master_id"]
        self.__floating = device_data["is_floating"]
        self.__props = Properties(device_data["props"], debug)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def master_id(self) -> int:
        return self.__master_id

    @property
    def floating(self) -> bool:
        return self.__floating

    @property
    def props(self) -> Properties:
        return self.__props

    @property
    def debug(self) -> bool:
        return self.__debug

    def query_state(self, loop=False) -> str:
        command = ["xinput", "query-state", str(self.id)]
        return get_command_output(command)

    def get_feedbacks(self, loop=False) -> str:
        command = ["xinput", "get-feedbacks", str(self.id)]
        return get_command_output(command)

    def set_prop(self, id_or_name: Union[int, str], new_value: str) -> None:
        required_property = self.props.get_property(id_or_name)
        required_property.change_value(new_value)

    def set_mode(self, mode: XInputDeviceMode) -> None:
        command = ["xinput", "set-mode", str(self.id), mode.name]
        run_command(command)

    def enable(self) -> None:
        self.set_prop("device_enabled", "1")

    def disable(self) -> None:
        self.set_prop("device_enabled", "0")

    def delete_property(self, prop_id_or_name: Union[int, str]) -> None:
        self.props.delete(prop_id_or_name)

    def __repr__(self) -> str:
        return f"XInputDevice(id={self.id}, name={self.name}, master_id={self.master_id}, props={self.props})"
