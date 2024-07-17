import subprocess

from ..parser import get_devices_data
from ..device.x_device import XInputDevice
from .pointer_buttons import XPointerButtons


class XPointer(XInputDevice):
    def __init__(self, pointer_data: dict, debug=False):
        super().__init__(pointer_data)
        self.buttons_map = XPointerButtons(
            pointer_data["id"], pointer_data["button_map"], debug=debug
        )

    def __getattr__(self, attr):
        if attr.startswith("disable_"):
            button_label_to_disable = attr.removeprefix("disable_")
            return lambda: self.buttons_map.disable_single(button_label_to_disable)
        elif attr.startswith("enable_"):
            button_label_to_enable = attr.removeprefix("enable_")
            return lambda: self.buttons_map.enable_single(button_label_to_enable)


def get_mouse_pointers(pointers_data: dict, debug=False):
    pointers = []
    for pointer_data in pointers_data.values():
        pointers.append(XPointer(pointer_data, debug=debug))
    return pointers
