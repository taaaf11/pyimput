import subprocess

from .device import XInputDevice
from .pointer import XPointer


def get_command_output(command: list):
    return subprocess.run(command, capture_output=True).stdout


run_command = subprocess.run


# not exactly a slug, but for naming ¯\_(ツ)_/¯
def slugify_label(label: str):
    slugified_label = label.lower().replace(" ", "_")
    return slugified_label


def clean_split(line_split: list[str]):
    useless_chars = "⎡⎜⎣↳"
    return [word for word in line_split if word not in useless_chars]


def get_prop_details_from_prop_line(dev_id: int, prop_line: str) -> dict:
    prop_details = {}
    prop_line_split = prop_line.split()
    for word in prop_line_split:
        if (
            word.startswith("(")
            and word.endswith(":")
            and word.strip("(:)").isnumeric()
        ):
            index_of_property: int = prop_line_split.index(word)

            prop_id = int(word.strip("(:)"))
            prop_name: str = "_".join(prop_line_split[:index_of_property]).lower()
            prop_values: list = " ".join(
                prop_line_split[(index_of_property + 1) :]
            ).split(",")
            prop_values: list = [prop_value.strip() for prop_value in prop_values]

            prop_details.update(
                {
                    prop_name: {
                        "dev_id": dev_id,
                        "prop_id": prop_id,
                        "prop_name": prop_name,
                        "values": prop_values,
                    }
                }
            )

    return prop_details


def get_all_devices(pointers_data: dict):
    devs = []
    for dev_data in pointers_data.values():
        if dev_data["button_map"] is None:
            devs.append(XInputDevice(dev_data))
        else:
            devs.append(XPointer(dev_data))
    return pointers
