from ..device import XInputDevice
from ..type import XInputDeviceCategory
from .keys import Keys


class XKeyboard(XInputDevice):
    def __init__(self, keyboard_data: dict, debug=False):
        super().__init__(keyboard_data, debug)
        self.__keys = Keys(keyboard_data["keycodes_map"])
        self.__category = XInputDeviceCategory.KEYBOARD
        self.__debug = debug

    @property
    def category(self) -> XInputDeviceCategory:
        return self.__category

    @property
    def debug(self) -> bool:
        return self.__debug

    @property
    def keys(self) -> list:
        return self.__keys

    def swap_keys(self, keycode_to_swap: int, keycode_to_swap_with: int):
        self.keys.swap_with(keycode_to_swap, keycode_to_swap_with)
