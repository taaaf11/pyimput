import subprocess
from src.py_xinput.userspace import get_all_devices
from src.py_xinput.parser import get_devices_data
from src.py_xinput.pointer import XPointer
from src.py_xinput.utils import get_command_output


def get_test_pointer():
    data = get_devices_data()
    for dev_data in data.values():
        if dev_data["button_map"] is None:
            continue
        if "XTEST" in dev_data["device_name"]:
            dev = XPointer(dev_data)
    return dev


# a test for both XPointer and XPointerButton classes
class TestXPointer:
    def test_disable_button(self):
        test_pointer = get_test_pointer()

        # prepare data
        test_pointer_buttons_map = test_pointer.disable_button_left()
        actual_pointer_buttons_map = get_command_output(['xinput', 'get-button-map', str(test_pointer.id)]).strip()

        # test
        assert test_pointer_buttons_map == actual_pointer_buttons_map

    # this also resets test_disable_button behaviour
    def test_enable_button(self):
        test_pointer = get_test_pointer()

        # prepare data
        test_pointer_buttons_map = test_pointer.disable_button_left()
        actual_pointer_buttons_map = get_command_output(['xinput', 'get-button-map', str(test_pointer.id)]).strip()

        # test
        assert test_pointer_buttons_map == actual_pointer_buttons_map
