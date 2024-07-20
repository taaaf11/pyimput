from parser import get_devices_data

from device import XInputDevice
from keyboard import XKeyboard
from pointer import XPointer

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


def get_devices_by_name(**kwargs):
    debug = kwargs.get("debug") or False
    all_devs = get_all_devices(debug)
    req_devs = []
    for arg, param in kwargs.items():
        for dev in all_devs:
            if arg == "eq":
                if dev.name == param:
                    return [dev]
            if arg in ["startswith", "endswith"]:
                dev_present = getattr(dev.name, arg)(param)
                if dev_present:
                    req_devs.append(dev)
            elif arg == "contains":
                if param in dev.name:
                    req_devs.append(dev)
    return req_devs


def get_devices_by_master(master_id: int, debug=False):
    all_devs = get_all_devices(debug)
    req_devs = []
    for dev in all_devs:
        if dev.master_id == master_id:
            req_devs.append(dev)
    return req_devs
