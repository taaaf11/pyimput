import subprocess

from ..type import ButtonsMapDict, OptionalString
from typing import Sequence


class XPointerButtons:
    def __init__(self, dev_id: int, buttons_map: dict, debug=False):
        self.dev_id = dev_id
        self.__buttons_map = buttons_map
        self.__debug = debug

    @property
    def buttons_map(self) -> ButtonsMapDict:
        return self.__buttons_map

    @property
    def debug() -> bool:
        return self.__debug

    def commit(self) -> OptionalString:
        button_states = self.buttons_map.values()
        button_states_str = " ".join([str(_) for _ in button_states])

        if self.debug:
            return button_states_str
        else:
            subprocess.run(
                ["xinput", "set-button-map", str(self.dev_id), button_states_str]
            )

    def enable_single(self, button_label: str) -> None:
        self.__buttons_map[button_label] = (
            list(self.buttons_map.keys()).index(button_label) + 1
        )

    def disable_single(self, button_label: str) -> None:
        self.__buttons_map[button_label] = 0

    def enable_multiple(self, button_labels: Sequence[str]) -> None:
        for label in button_labels:
            self.__buttons_map[label] = list(self.buttons_map.keys()).index(label) + 1

    def disable_multiple(self, button_labels: Sequence[str]) -> None:
        for label in labels:
            self.__buttons_map[label] = 0

    def __repr__(self) -> str:
        return f"XPointerButtons(dev_id={self.dev_id}, buttons_map={list(self.buttons_map.values())})"
