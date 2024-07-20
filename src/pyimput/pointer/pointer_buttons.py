import subprocess
from typing import Sequence

from type import ButtonsMapDict, OptionalString


class XPointerButtons:
    def __init__(self, dev_id: int, buttons_map: dict, debug=False):
        self.dev_id = dev_id
        self.__buttons_map = buttons_map
        self.__debug = debug

    @property
    def buttons_map(self) -> ButtonsMapDict:
        return self.__buttons_map

    @property
    def available_buttons(self) -> list:
        buttons = []
        for button_label in self.buttons_map.keys():
            better_label = " ".join(
                label.capitalize() for label in button_label.replace("_", " ").split()
            )
            buttons.append(better_label)
        return buttons

    @property
    def debug(self) -> bool:
        return self.__debug

    def commit(self) -> OptionalString:
        button_states = self.buttons_map.values()
        button_states_str = " ".join([str(_) for _ in button_states])

        if not self.debug:
            subprocess.run(
                ["sh", "-c", f"xinput set-button-map {self.dev_id} {button_states_str}"]
            )
        return button_states_str

    def swap_with(self, button_label_to_swap: str, button_label_to_swap_with: str):
        temp = self.buttons_map[button_label_to_swap]
        self.buttons_map[button_label_to_swap] = self.buttons_map[
            button_label_to_swap_with
        ]
        self.buttons_map[button_label_to_swap_with] = temp
        self.commit()

    def enable_single(self, button_label: str) -> None:
        self.__buttons_map[button_label] = (
            list(self.buttons_map.keys()).index(button_label) + 1
        )
        self.commit()

    def disable_single(self, button_label: str) -> None:
        self.__buttons_map[button_label] = 0
        self.commit()

    def __repr__(self) -> str:
        return f"XPointerButtons(dev_id={self.dev_id}, buttons_map={list(self.buttons_map.values())})"
