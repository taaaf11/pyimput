import subprocess
from collections import UserList
from dataclasses import dataclass

from typing import Union


@dataclass
class Property:
    id: int
    name: str
    dev_id: int
    values: list[str]
    debug: False

    def change_value(self, new_value: str) -> None:
        self.values = new_value.split(" ")
        if self.debug:
            return self.values
        else:
            subprocess.run(["xinput", "set-prop", str(self.dev_id), str(self.id), new_value])


class Properties(UserList):
    def __init__(self, props_dict: dict, debug=False) -> None:
        self.__prop_ids = []
        self.__prop_names = []
        props = []
        for key, value in props_dict.items():
            prop_id = value["prop_id"]
            prop_name = key
            prop_dev_id = value["dev_id"]
            prop_values = value["values"]

            prop = Property(prop_id, prop_name, prop_dev_id, prop_values, debug)

            self.__prop_ids.append(prop_id)
            self.__prop_names.append(prop_name)

            props.append(prop)

        super().__init__(props)

        self.__debug = debug

    def _get_property_by_id(self, id: int) -> Property:
        for property in self.data:
            if property.id == id:
                return property

    def _get_property_by_name(self, name: str) -> Property:
        for property in self.data:
            if property.name == name:
                return property

    def get_property(self, prop_id_or_name: Union[int, str]) -> Property:
        if isinstance(prop_id_or_name, int):
            return self._get_property_by_id(prop_id_or_name)
        elif isinstance(prop_id_or_name, str):
            return self._get_property_by_name(prop_id_or_name)

    def delete(self, prop_id_or_name: Union[int, str]) -> None:
        required_property = self.get_property(prop_id_or_name)
        if self.__debug:
            self.data.remove(required_property)
            return self.data
        else:
            subprocess.run(
                [
                    "xinput",
                    "delete-prop",
                    str(required_property.dev_id),
                    str(required_property.id),
                ]
            )
            self.data.remove(required_property)

    def __contains__(self, item: Union[int, str, Property]) -> bool:
        if isinstance(item, int):
            return item in self.__prop_ids
        elif isinstance(item, str):
            return item in self.__prop_names
        elif isinstance(item, Property):
            return item in self.data
