from collections import UserDict
from types import MappingProxyType
from typing import Optional

from utils import run_command


class Keys(UserDict):
    def __init__(self, keycodes_dict: Optional[dict], debug=False):
        self.__data = keycodes_dict or {}
        self.__debug = False

    @property
    def debug(self) -> bool:
        return self.__debug

    @property
    def data(self) -> MappingProxyType[dict]:
        return MappingProxyType(self.__data)

    def swap_with(self, keycode_to_swap: int, keycode_to_swap_with: int):
        temp = self.data[keycode_to_swap]

        command = f'xmodmap -e "keycode {keycode_to_swap} = {self.data[keycode_to_swap_with]}"'
        self.__data[keycode_to_swap] = self.data[keycode_to_swap_with]
        run_command(
            ["sh", "-c", command]
        )

        command = f'xmodmap -e "keycode {keycode_to_swap_with} = {temp}"'
        self.__data[keycode_to_swap_with] = temp
        run_command(
            ["sh", "-c", command]
        )

    def __setitem__(self, key, item) -> None:
        raise NotImplementedError()

    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __contains__(self, item: int) -> bool:
        return item in self.data

    def __repr__(self) -> str:
        return f"Keys({self.data})"
