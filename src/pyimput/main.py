#!/usr/bin/python3

import sys
from argparse import ArgumentParser as AG

from .type import XInputDeviceCategory as XInputDeviceCategory
from .userspace import *
from .utils import get_keys_with_types, get_keysyms_enumeration

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
            [dev for dev in all_devs if dev.category == XInputDeviceCategory.POINTER],
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
            [dev for dev in all_devs if dev.category == XInputDeviceCategory.KEYBOARD],
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
            [dev for dev in all_devs if dev.category == XInputDeviceCategory.OTHER],
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
    options_available = [
        "Enable this device.",
        "Disable this device.",
        "Swap buttons.",
        "See available buttons.",
    ]

    count_opts_map = dict(enumerate(options_available, start=1))

    print("Available options:")
    for count, option in count_opts_map.items():
        print(f"{count}. {option}")


def print_available_device_buttons(dev):
    print("\nAvailable buttons:")
    if dev.category == XInputDeviceCategory.POINTER:
        count_label_map = dict(enumerate(dev.available_buttons(), start=1))
        print(
            "\n".join([f"{count}. {label}" for count, label in count_label_map.items()])
        )

        return count_label_map

    elif dev.category == XInputDeviceCategory.KEYBOARD:
        keycodes = get_keys_with_types()
        count_keycodes_map = get_keysyms_enumeration(keycodes)
        count = 0

        print("Alphabets:")
        for keycode, keysym_sem in keycodes["alphabets"].items():
            count += 1
            print(f"{count}. {keysym_sem} ({keycode})")

        print("\nNumbers:")
        for keycode, keysym_sem in keycodes["numbers"].items():
            count += 1
            print(f"{count}. {keysym_sem} ({keycode})")

        print("\nSpecial characters:")
        for keycode, keysym_sem in keycodes["special"].items():
            count += 1
            print(f"{count}. {keysym_sem} ({keycode})")

        return count_keycodes_map


def swapper_cli(dev) -> None:
    count_map = print_available_device_buttons(dev)
    swap_choices = input("Enter button numbers to be swapped (as 2 3;4 5): ")

    for choice in swap_choices.split(";"):
        num_to_swap, num_to_be_swapped_with = choice.split(" ")
        if dev.category == XInputDeviceCategory.POINTER:
            label_to_swap, label_to_be_swapped_with = (
                count_map[int(num_to_swap)],
                count_map[int(num_to_be_swapped_with)],
            )
            label_to_swap = label_to_swap.replace(" ", "_").lower()
            label_to_be_swapped_with = label_to_be_swapped_with.replace(
                " ", "_"
            ).lower()

            dev.swap_with(label_to_swap, label_to_be_swapped_with)

        elif dev.category == XInputDeviceCategory.KEYBOARD:
            keycode_to_swap, keycode_to_swap_with = (
                count_map[int(num_to_swap)][0],
                count_map[int(num_to_be_swapped_with)][0],
            )

            dev.swap_keys(keycode_to_swap, keycode_to_swap_with)


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
            swapper_cli(selected_device)
        case 4:
            print_available_device_buttons(selected_device)
        case _:
            print("\nUnknown option.")
            sys.exit(1)

    options_available = []


def main():
    all_devices = [
        dev
        for dev in get_all_devices()
        if "XTEST" not in dev.name and ((dev.master_id is not None) or (dev.floating))
    ]

    dev_id_dev_map = dict({dev.id: dev for dev in all_devices})

    if len(sys.argv) == 1:
        try:
            start_cli(all_devices, dev_id_dev_map)
        except KeyboardInterrupt:
            sys.exit(1)

    parser = AG()

    apko_group = parser.add_mutually_exclusive_group()
    apko_group.add_argument(
        "-a", "--all-devices", help="Get info about all devices.", action="store_true"
    )
    apko_group.add_argument(
        "-p",
        "--pointers",
        help="Get info about all pointer devices.",
        action="store_true",
    )
    apko_group.add_argument(
        "-k",
        "--keyboards",
        help="Get info about all keyboard devices.",
        action="store_true",
    )
    apko_group.add_argument(
        "-o", "--other", help="Get info about all other devices.", action="store_true"
    )

    parser.add_argument(
        "--id",
        nargs="+",
        type=str,
        help="A space separated list of id's of devices to work with.",
    )

    parser.add_argument("-d", "--disable", nargs="+", type=str, help="Disable device.")
    parser.add_argument("-e", "--enable", nargs="+", type=str, help="Enable device.")

    args = parser.parse_args()

    query_devs_opts = any([args.all_devices, args.pointers, args.keyboards, args.other])
    enable_disable_opts = any([args.enable, args.disable])

    if enable_disable_opts and not args.id:
        ...

    if query_devs_opts:
        if args.all_devices:
            print_all_devs_with_numbers(all_devices)
        elif args.pointers:
            print_pointers_with_numbers(all_devices)
        elif args.keyboards:
            print_keyboards_with_numbers(all_devices)
        elif args.other:
            print_other_devs_with_numbers(all_devices)
        sys.exit(0)

    if enable_disable_opts:
        id_or_names = args.enable or args.disable
        if args.enable:
            selected_devices = []
            for id_or_name in id_or_names:
                try:
                    id_ = int(id_or_name)
                    selected_device = [dev for dev in all_devices if dev.id == id_][0]
                    selected_devices.append(selected_device)
                    selected_device.disable()
                except ValueError:
                    name = id_or_name
                    devs_with_name = get_devices_by_name(contains=name)
                    selected_devices.expand(devs_with_name)
                for dev in selected_devices:
                    dev.enable()

        if args.disable:
            selected_devices = []
            for id_or_name in id_or_names:
                try:
                    id_ = int(id_or_name)
                    selected_device = [dev for dev in all_devices if dev.id == id_][0]
                    selected_devices.append(selected_device)
                    selected_device.disable()
                except ValueError:
                    name = id_or_name
                    devs_with_name = get_devices_by_name(contains=name)
                    selected_devices.expand(devs_with_name)
                for dev in selected_devices:
                    dev.disable()


if __name__ == "__main__":
    main()
