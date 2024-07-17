import subprocess
from .properties import Properties


class XInputDevice:
    def __init__(self, device_data: dict):
        self.__id = device_data['id']
        self.__name = device_data['device_name']
        self.__master_id = device_data['master_id']
        self.__props = Properties(device_data['props'])

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def master_id(self):
        return self.__master_id

    @property
    def props(self):
        return self.__props

    def set_prop(self, id_or_name: int | str, new_value: str):
        required_property = self.props.get_property(id_or_name)
        required_property.change_value(new_value)

    def __repr__(self):
        return f"XInputDevice(id={self.id}, name={self.name}, master_id={self.master_id}, props={self.props})"


#    def enable(self, ...):
        
#        ...

#    def disable(self, ...):
#        ...
