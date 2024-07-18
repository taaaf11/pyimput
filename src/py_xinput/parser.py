import subprocess
from .type import DeviceDataDict, PropsDict, ButtonsMapDict

from .utils import (clean_split, get_command_output,
                    get_prop_details_from_prop_line, slugify_label)


def get_pointer_button_map(dev_id: int) -> ButtonsMapDict:
    dev_classes = (
        get_command_output(["xinput", "list", str(dev_id)]).split("\n")
    )

    supported_button_labels = dev_classes[4].split(":")[1].strip().split('"')
    supported_button_labels = [
        slugify_label(sup_label)
        for sup_label in supported_button_labels
        if sup_label.replace(" ", "").isalpha()
    ]

    for sup_button_label in supported_button_labels.copy():
        if "none" in sup_button_label:
            split = sup_button_label.strip('_').split('_')
            for none_c, none in enumerate(split):
                supported_button_labels.append(none+'_'+str(none_c))
            supported_button_labels.remove(sup_button_label)

    button_map = dict(
        list(
            [(value, key) for key, value in enumerate(supported_button_labels, start=1)]
        )
    )

    return button_map


def get_device_props(dev_id: int) -> PropsDict:
    dev_props = {}
    dev_prop_lines = (
        get_command_output(["xinput", "list-props", str(dev_id)])
        .split("\n")[1:]
    )

    for dev_prop_line in dev_prop_lines:
        dev_props.update(get_prop_details_from_prop_line(dev_id, dev_prop_line))

    return dev_props


def get_devices_data() -> DeviceDataDict:
    xinput_list_out_lines = (
        get_command_output(["xinput", "list"]).split("\n")[:-1]
    )  # last one is empty string
    devs_data = {}
    dev_count = 0
    is_pointer = False

    for output_line in xinput_list_out_lines:
        if "Virtual core pointer" in output_line:
            is_pointer = True
            continue
        if "Virtual core keyboard" in output_line:
            is_pointer = False
            continue

        line_split = clean_split(output_line.split())

        dev_id = int(line_split[-4][3:])
        dev_master_id = int(line_split[-1][1:][:-2])
        dev_name = " ".join(line_split[:-4])
        dev_props = get_device_props(dev_id)

        dev_count += 1

        if is_pointer:
            button_map = get_pointer_button_map(dev_id)
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
        if is_pointer:
            print(f"Device name: {dev_name}, button_map: {button_map}")

    return devs_data
