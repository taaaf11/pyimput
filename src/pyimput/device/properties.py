import subprocess
from collections import UserList
from dataclasses import dataclass
from typing import List, Union


class Property:
    def __init__(
        self, id: int, name: str, dev_id: int, values: list[str], debug: False
    ):
        self.__id = id
        self.__name = name
        self.__dev_id = dev_id
        self.__values = values

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def dev_id(self) -> int:
        return self.__dev_id

    @property
    def values(self) -> List[str]:
        return self.__values

    def change_value(self, new_value: str) -> None:
        self.__values = new_value.split(" ")
        if self.debug:
            return self.values
        else:
            subprocess.run(
                ["sh", "-c", f"xinput set-prop {self.dev_id} {self.id} {new_value}"]
            )


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
        return False
