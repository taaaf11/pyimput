from .keyboard import XKeyboard
from .pointer import XPointer
from .parser import get_devices_data


__all__ = ['get_all_devices', 'get_all_pointers', 'get_all_keyboards', 'get_device_by_id', 'get_devices_by_name', 'get_devices_by_master']

def get_all_devices(debug=False):
    data = get_devices_data()
    devs = []
    for dev_data in data.values():
        if dev_data["button_map"] is None:
            devs.append(XKeyBoard(dev_data, debug=debug))
        else:
            devs.append(XPointer(dev_data, debug=debug))
    return devs

def get_all_pointers(debug=False):
    all_devs = get_all_devices(debug)
    pointers = []
    for dev in all_devs:
        if dev.__class__.__name__ == 'XPointer':
            pointers.append(dev)
    return pointers

def get_all_keyboards(debug=False):
    all_devs = get_all_devices(debug)
    keyboards = []
    for dev in all_devs:
        if dev.__class__.__name__ == 'XKeyboard':
            keyboards.append(dev)
    return keyboards

def get_device_by_id(id: int, debug=False):
    all_devices = get_all_devices(debug)
    for dev in all_devs:
        if dev.id == id:
            return dev

def get_devices_by_name(**kwargs):
    debug = kwargs.get('debug') or False
    all_devs = get_all_devices(debug)
    req_devs = []
    for arg, param in kwargs.items():
        for dev in all_devs:
            if arg == 'eq':
                if dev.name == param:
                    return [dev]
            if arg in ['startswith', 'endswith']:
                dev_present = getattr(dev.name, arg)(param)
                if dev_present:
                    req_devs.append(dev)
            elif arg == 'contains':
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
    
