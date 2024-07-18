import subprocess

from ..type import XInputDeviceMode
from .properties import Properties

# fix circular import
# from ..utils import get_command_output, run_command



# fix circular import
def get_command_output(command: list):
    return subprocess.run(command, capture_output=True).stdout


run_command = subprocess.run


class XInputDevice:
    def __init__(self, device_data: dict):
        self.__id = device_data["id"]
        self.__name = device_data["device_name"]
        self.__master_id = device_data["master_id"]
        self.__props = Properties(device_data["props"])

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def master_id(self):
        return self.__master_id

    @property
    def props(self):
        return self.__props

    def query_state(self, loop=False):
        command = ["xinput", "query-state", str(dev_id)]
        if loop:
            while True:
                output = get_command_output(command)
                print(output)
        else:
            output = get_command_output(command)
            print(output)

    def get_feedbacks(self, loop=False):
        command = ["xinput", "get-feedbacks", str(dev_id)]
        if loop:
            while True:
                output = get_command_output(command)
                print(output)
        else:
            output = get_command_output(command)
            print(output)

    def set_prop(self, id_or_name: int | str, new_value: str):
        required_property = self.props.get_property(id_or_name)
        required_property.change_value(new_value)

    def set_mode(self, mode: XInputDeviceMode):
        command = ["xinput", "set-mode", str(dev_id), mode.name]
        run_command(command)

    def set_floating(self):
        command = ["xinput", "float", str(dev_id)]
        run_command(command)

    def reattach(self, master_id: None):
        master_id = x or self.master_id
        command = ["xinput", "reattach", str(self.dev_id), str(master_id)]
        run_command(command)

    def enable(self):
        self.set_prop("device_enabled", "1")

    def disable(self):
        self.set_prop("device_enabled", "0")

    def delete_property(self, prop_id_or_name: int | str):
        self.props.delete(prop_id_or_name)

    def __repr__(self):
        return f"XInputDevice(id={self.id}, name={self.name}, master_id={self.master_id}, props={self.props})"
