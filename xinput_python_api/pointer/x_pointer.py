import subprocess

from ..device.x_device import XInputDevice
from .pointer_buttons import XPointerButtons


class XPointer(XInputDevice):
    def __init__(self, pointer_data: dict, debug=False):
        super().__init__(pointer_data)
        self.__buttons_map = XPointerButtons(
            pointer_data["id"], pointer_data["button_map"], debug=debug
        )

    @property
    def buttons_map(self):
        return self.__buttons_map

    def __getattr__(self, attr):
        if attr.startswith("disable_"):
            button_label_to_disable = attr.removeprefix("disable_")
            return lambda: self.buttons_map.disable_single(button_label_to_disable)
        elif attr.startswith("enable_"):
            button_label_to_enable = attr.removeprefix("enable_")
            return lambda: self.buttons_map.enable_single(button_label_to_enable)

    def __repr__(self):
        return f"XPointer(id={self.id}, name={self.name}, master_id={self.master_id}, buttons_map={self.buttons_map})"
