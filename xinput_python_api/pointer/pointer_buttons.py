import subprocess


class XPointerButtons:
    def __init__(self, dev_id: int, buttons_map: dict, debug=False):
        self.dev_id = dev_id
        self.__buttons_map = buttons_map
        self.debug = debug
    
    @property
    def buttons_map(self):
        return self.__buttons_map

    def commit(self):
        button_states = self.buttons_map.values()
        button_states_str = " ".join([str(_) for _ in button_states])

        if self.debug:
            print(button_states_str)
        else:
            subprocess.run(
                ["xinput", "set-button-map", str(self.dev_id), button_states_str]
            )

    def enable_single(self, button_label: str):
        self.__buttons_map[button_label] = (
            list(self.buttons_map.keys()).index(button_label) + 1
        )

    def enable_multiple(self, button_labels: list[str]):
        for label in button_labels:
            self.__buttons_map[label] = list(self.buttons_map.keys()).index(label) + 1

    def disable_single(self, button_label: str):
        self.__buttons_map[button_label] = 0

    def disable_multiple(self, button_labels: list[str]):
        for label in labels:
            self.__buttons_map[label] = 0

    def __repr__(self):
        return f"XPointerButtons(dev_id={self.dev_id}, buttons_map={list(self.buttons_map.values())})"
