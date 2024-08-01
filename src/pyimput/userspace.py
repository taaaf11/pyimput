from .device import XInputDevice
from .keyboard import XKeyboard
from .parser import get_devices_data
from .pointer import XPointer
from .type import GetByNameMethod

__all__ = [
    "get_all_devices",
    "get_all_master_devices",
    "get_device_by_id",
    "get_devices_by_name",
    "get_devices_by_master",
]


def get_all_devices(debug=False):
    data = get_devices_data()
    devs = []
    for dev_data in data.values():
        dev_name = dev_data["device_name"]
        if "Keyboard" in dev_name:
            devs.append(XKeyboard(dev_data, debug=debug))
        elif "Mouse" in dev_name:
            devs.append(XPointer(dev_data, debug=debug))
        else:
            devs.append(XInputDevice(dev_data, debug=debug))
    return devs


def get_all_master_devices(debug=False):
    return [dev for dev in get_all_devices(debug) if dev.master_id is None]


def get_device_by_id(id: int, debug=False):
    all_devices = get_all_devices(debug)
    for dev in all_devs:
        if dev.id == id:
            return dev


def get_devices_by_name(name: str, method: GetByNameMethod = GetByNameMethod.EQ, debug=False):
    all_devs = get_all_devices(debug)
    req_devs = []
    for dev in all_devs:
        if method == GetByNameMethod.CONTAINS:
            if name in dev.name:
                req_devs.append(dev)
        if method == GetByNameMethod.EQ:
            if name == dev.name:
                req_devs.append(dev)
    return req_devs


def get_devices_by_master(master_id: int, debug=False):
    all_devs = get_all_devices(debug)
    req_devs = []
    for dev in all_devs:
        if dev.master_id == master_id:
            req_devs.append(dev)
    return req_devs
