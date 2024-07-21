#!/usr/bin/python3

import sys
from argparse import ArgumentParser as AG

from userspace import *

PROG_NAME = "pyimput"
PROG_NAME_STYLED = """
             _                       _
            (_)                     | |
 _ __  _   _ _ _ __ ___  _ __  _   _| |_
| '_ \| | | | | '_ ` _ \| '_ \| | | | __|
| |_) | |_| | | | | | | | |_) | |_| | |_
| .__/ \__, |_|_| |_| |_| .__/ \__,_|\__|
| |     __/ |           | |
|_|    |___/            |_|
"""


def print_pointers_with_numbers(all_devs: list):
    pointers = dict(
        enumerate(
            [dev for dev in all_devs if dev.__class__.__name__ == "XPointer"],
            start=1,
        )
    )

    print("Attached pointers:")
    for count, pointer in pointers.items():
        print(
            f"{count}. {pointer.name} (id = {pointer.id}, master id = {pointer.master_id}, floating = {pointer.floating})"
        )

    return pointers


def print_keyboards_with_numbers(all_devs: list):
    keyboards = dict(
        enumerate(
            [dev for dev in all_devs if dev.__class__.__name__ == "XKeyboard"],
            start=1,
        )
    )

    print("Attached keyboards:")
    for count, keyboard in keyboards.items():
        print(
            f"{count}. {keyboard.name} (id = {keyboard.id}, master id = {keyboard.master_id}, floating = {keyboard.floating})"
        )

    return keyboards


def print_other_devs_with_numbers(all_devs: list):
    other_devs = dict(
        enumerate(
            [dev for dev in all_devs if dev.__class__.__name__ == "XInputDevice"],
            start=1,
        )
    )

    print("Other attached devices:")
    for count, other_dev in other_devs.items():
        print(
            f"{count}. {other_dev.name} (id = {other_dev.id}, master id = {other_dev.master_id}, floating = {other_dev.floating})"
        )

    return other_devs


def print_all_devs_with_numbers(all_devs: list):
    print_pointers_with_numbers(all_devs)
    print("\n", end="")

    print_keyboards_with_numbers(all_devs)
    print("\n", end="")
    
    print_other_devs_with_numbers(all_devs)
    print("\n", end="")


def print_dev_options(dev):
    options_avail = ["Enable this device.", "Disable this device."]  # available for all devices
    options_avail_pointer = ["Swap buttons.", "See available buttons."]  # specific to pointers (yet, maybe)

    options_available = options_avail
    if dev.__class__.__name__ == "XPointer":
        options_available.extend(options_avail_pointer)

    count_opts_map = dict(enumerate(options_available, start=1))

    print("Available options:")
    for count, option in count_opts_map.items():
        print(f"{count}. {option}")


def print_available_pointer_buttons(pointer):
    print("\nAvailable buttons:")
    count_label_map = dict(
        enumerate(pointer.available_buttons(), start=1)
    )
    print(
        "\n".join(
            [
                f"{count}. {label}"
                for count, label in count_label_map.items()
            ]
        )
    )


def start_cli(all_devices, dev_id_dev_map):
    print(PROG_NAME_STYLED)
    print("\n\n", end="")
    print_all_devs_with_numbers(all_devices)
    try:
        selected_device = dev_id_dev_map.get(
            int(input("\nSelect a device (id) to work with: "))
        )
    except ValueError:
        print("\nPlease enter valid device id.")
        sys.exit(1)

    if selected_device is None:
        print("\nNo such device.")
        sys.exit(1)
    
    print_dev_options(selected_device)
    selected_choice = int(input("\nYour choice: "))

    match selected_choice:
        case 1:
            selected_device.enable()
        case 2:
            selected_device.disable()
        case 3:
            print_available_pointer_buttons(selected_device)
            selected_swap_choices = [
                int(_)
                for _ in input(
                    "Enter any two of the numbers of available buttons above, separated by space: "
                ).split()
            ]
            selected_swapping_labels = [
                count_label_map[_].replace(" ", "_").lower()
                for _ in selected_swap_choices
            ]
            selected_device.swap_with(*selected_swapping_labels)
        case 4:
            print_available_pointer_buttons(selected_device)
        case _:
            print("\nUnknown option.")
            sys.exit(1)

    options_available = []


def disable_device(dev_id_or_name: int | str):
    ...


def enable_device(dev_id_or_name: int | str):
    ...


def main():
    all_devices = [
        dev
        for dev in get_all_devices()
        if "TEST" not in dev.name and ((dev.master_id is not None) or (dev.floating))
    ]

    dev_id_dev_map = dict({dev.id: dev for dev in all_devices})

    if len(sys.argv) == 1:
        start_cli(all_devices, dev_id_dev_map)

    parser = AG()

    apko_group = parser.add_mutually_exclusive_group()
    apko_group.add_argument("-a", "--all-devices", help="Get info about all devices.", action="store_true")
    apko_group.add_argument(
        "-p", "--pointers", help="Get info about all pointer devices.", action="store_true"
    )
    apko_group.add_argument(
        "-k", "--keyboards", help="Get info about all keyboard devices.", action="store_true"
    )
    apko_group.add_argument("-o", "--other", help="Get info about all other devices.", action="store_true")

    parser.add_argument("-d", "--disable", type=str, help="Disable device.")
    parser.add_argument("-e", "--enable", type=str, help="Enable device.")

    args = parser.parse_args()
    
    if args.all_devices:
        print_all_devs_with_numbers(all_devices)
    elif args.pointers:
        print_pointers_with_numbers(all_devices)
    elif args.keyboards:
        print_keyboards_with_numbers(all_devices)
    elif args.other:
        print_other_devs_with_numbers(all_devices)

if __name__ == "__main__":
    main()
