import subprocess

from ..device import XInputDevice
from ..type import ButtonsMapDict, DeviceDataDict, XInputDeviceCategory

from .pointer_buttons import XPointerButtons


class XPointer(XInputDevice):
    def __init__(self, pointer_data: DeviceDataDict, debug=False) -> None:
        super().__init__(pointer_data)
        self.__buttons_map = XPointerButtons(
            pointer_data["id"], pointer_data["button_map"], debug=debug
        )
        self.__category = XInputDeviceCategory.POINTER
        self.change_button_map = lambda: setattr(
            self,
            "__buttons_map",
            XPointerButtons(
                pointer_data["id"],
                pointer_data["button_map"],
                self.__buttons_map.buttons_map,
            ),
        )

    @property
    def buttons_map(self) -> ButtonsMapDict:
        return self.__buttons_map

    @property
    def category(self) -> XInputDeviceCategory:
        return self.__category

    def swap_with(self, button_label_to_swap: str, button_label_to_swap_with: str):
        self.buttons_map.swap_with(button_label_to_swap, button_label_to_swap_with)
        self.buttons_map.commit()

    def __getattr__(self, attr):
        if attr.startswith("enable_") or attr.startswith("disable_"):
            if attr.startswith("disable_"):
                button_label_to_disable = attr.removeprefix("disable_")
                self.buttons_map.disable_single(button_label_to_disable)
            elif attr.startswith("enable_"):
                button_label_to_enable = attr.removeprefix("enable_")
                self.buttons_map.enable_single(button_label_to_enable)
            self.change_button_map()

            return lambda: self.buttons_map.commit()
        else:
            return lambda: getattr(self.buttons_map, attr)
        return super().__getattr__(attr)
        # raise AttributeError(f"'{self.__name__}' has no attribute '{attr}'")

    def __repr__(self) -> str:
        return f"XPointer(id={self.id}, name={self.name}, master_id={self.master_id}, buttons_map={self.buttons_map})"
