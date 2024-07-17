import subprocess


class XPointerButtons:
    def __init__(self, dev_id: int, buttons_map: dict, debug=False):
        self.dev_id = dev_id
        self.buttons_map = buttons_map
        self.debug = debug

    def _commit(self):
        button_states = self.buttons_map.values()
        button_states_str = " ".join([str(_) for _ in button_states])

        if self.debug:
            return button_states_str
        else:
            subprocess.run(
                ["xinput", "set-button-map", str(self.dev_id), button_states_str]
            )

    def enable_single(self, button_label: str):
        self.buttons_map[button_label] = (
            list(self.buttons_map.keys()).index(button_label) + 1
        )

        self._commit()

    def enable_multiple(self, button_labels: list[str]):
        for label in button_labels:
            self.buttons_map[label] = list(self.buttons_map.keys()).index(label) + 1

        self._commit()

    def disable_single(self, button_label: str):
        self.buttons_map[button_label] = 0

        self._commit()

    def disable_multiple(self, button_labels: list[str]):
        for label in labels:
            self.buttons_map[label] = 0

        self._commit()

    def __repr__(self):
        return f"XPointerButtons(dev_id={self.dev_id}, buttons_map={self.buttons_map.values()})"
