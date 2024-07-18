from .device import XInputDevice
from .pointer import XPointer
from .parser import get_devices_data


def get_all_devices():
    data = get_devices_data()
    devs = []
    for dev_data in data.values():
        if dev_data["button_map"] is None:
            devs.append(XInputDevice(dev_data))
        else:
            devs.append(XPointer(dev_data))
    return devs

def get_test_pointer():
    all_devs = get_all_devices()
    for dev in all_devs:
        if dev.__class__.__name__ == "XPointer" and "XTEST" in dev.name:
            return dev
