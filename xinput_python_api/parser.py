import subprocess

from utils import (clean_split, get_command_output,
                    get_prop_details_from_prop_line, slugify_label)


def get_mouse_button_map(dev_id: int) -> dict:
    dev_classes = (
        get_command_output(["xinput", "list", str(dev_id)]).decode().split("\n")
    )

    supported_button_labels = dev_classes[4].split(":")[1].strip().split('"')
    supported_button_labels = [
        slugify_label(sup_label)
        for sup_label in supported_button_labels
        if sup_label.replace(" ", "").isalpha()
    ]

    button_map = dict(
        list(
            [(value, key) for key, value in enumerate(supported_button_labels, start=1)]
        )
    )

    return button_map


def get_device_props(dev_id: int) -> dict:
    dev_props = {}
    dev_prop_lines = (
        get_command_output(["xinput", "list-props", str(dev_id)])
        .decode()
        .split("\n")[1:]
    )

    for dev_prop_line in dev_prop_lines:
        dev_props.update(get_prop_details_from_prop_line(dev_prop_line))

    return dev_props


def get_devices_data():
    xinput_list_out_lines = get_command_output(["xinput", "list"]).decode().split("\n")[:-1]  # last one is empty string
    pointer_started = False
    dev_count = 0
    devs_data = {}

    for output_line in xinput_list_out_lines:
        if "Virtual core pointer" in output_line:
            pointer_started = True
            continue
        if "Virtual core keyboard" in output_line:
            pointer_started = False
            continue

        line_split = clean_split(output_line.split())

        dev_id = int(line_split[-4][3:])
        dev_master_id = int(line_split[-1][1:][:-2])
        dev_name = " ".join(line_split[:-4])
        dev_props = get_device_props(dev_id)

        dev_count += 1

        if pointer_started:
            button_map = get_mouse_button_map(dev_id)
        else:
            button_map = None

        devs_data.update(
            {
                dev_count: {
                    "id": dev_id,
                    "master_id": dev_master_id,
                    "device_name": dev_name,
                    "button_map": button_map,
                    "props": dev_props,
                }
            }
        )

    return devs_data


if __name__ == "__main__":
    print(get_devices_data())
