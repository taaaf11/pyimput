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


def main():
    all_devices = [dev for dev in get_all_devices() if 'TEST' not in dev.name and ((dev.master_id is not None) or (dev.floating))]
    options_avail_pointer = ["Swap buttons.", "See available buttons."]
    options_avail = ["Enable this device.", "Disable this device."]
    count_dev_map = dict(enumerate(all_devices, start=1))
    if len(sys.argv) == 1:
        print(PROG_NAME_STYLED)
        print("\n\n", end="")
        print("Devices:")
        for key, value in count_dev_map.items():
            dev = value
            dev_class = dev.__class__.__name__
            match dev_class:
                case 'XPointer':
                    dev_type = 'Pointer'
                case 'XKeyboard':
                    dev_type = 'Keyboard'
                case _:
                    dev_type = 'Other'
            print(f"{key}. {dev.name} (id = {dev.id}, master id = {dev.master_id}, floating = {dev.floating}, type = {dev_type})")
        try:
            selected_device = count_dev_map.get(int(input("\nSelect a device to work with: ")))
        except ValueError:
            print("\nPlease enter valid device number.")
            sys.exit(1)
        
        if selected_device is None:
            print("\nNo such device.")
            sys.exit(1)

        print("\nAvailable options:")

        options_available = options_avail
        if selected_device.__class__.__name__ == 'XPointer':
            options_available += options_avail_pointer

        count_opts_map = dict(enumerate(options_available, start=1))
        print('\n'.join([f"{count}. {option}" for count, option in count_opts_map.items()]))

        selected_choice = int(input("\nYour choice: "))

        match selected_choice:
            case 1:
                selected_device.enable()
            case 2:
                selected_device.disable()
            case 3:
                print("\nAvailable buttons:")
                count_label_map = dict(enumerate(selected_device.available_buttons(), start=1))
                print("\n".join([f"{count}. {label}" for count, label in count_label_map.items()]))
                selected_swap_choices = [int(_) for _ in input("Enter any two of the numbers of available buttons above, separated by space: ").split()]
                selected_swapping_labels = [count_label_map[_].replace(" ", "_").lower() for _ in selected_swap_choices]
                selected_device.swap_with(*selected_swapping_labels)
            case 4:
                print("\nAvailable buttons:")
                count_label_map = dict(enumerate(selected_device.available_buttons(), start=1))
                print("\n".join([f"{count}. {label}" for count, label in count_label_map.items()]))
            case _:
                print("\nUnknown option.")
                sys.exit(1)
            

        options_available = []

    parser = AG()

    apko_group = parser.add_mutually_exclusive_group()
    apko_group.add_argument("-a", "--all-devices", help="Get info about all devices.")
    apko_group.add_argument("-p", "--pointers", help="Get info about all pointer devices.")
    apko_group.add_argument("-k", "--keyboards", help="Get info about all keyboard devices.")
    apko_group.add_argument("-o", "--other", help="Get info about all other devices.")


    
    parser.add_argument("-d", "--disable", type=int | str, help="Disable device.")
    parser.add_argument("-e", "--enable", type=int | str, help="Enable device.")
    parser.
    
    parser.parse_args()


if __name__ == "__main__":
    main()
