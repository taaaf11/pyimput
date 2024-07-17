from collections import UserList
from dataclasses import dataclass
import subprocess

@dataclass
class Property:
    id: int
    name: str
    dev_id: int
    values: list[str]

    def change_value(new_value: str):
        self.values = new_value.split(' ')
        subprocess.run(['xinput', 'set-prop', str(dev_id), str(id), new_value])


class Properties(UserList):
    def __init__(self, props_dict: dict):
        self.prop_ids = []
        self.prop_names = []
        props = []
        for key, value in props_dict.items():
            prop_id = value['prop_id']
            prop_name = key
            prop_dev_id = value['dev_id']
            prop_values = value['values']

            prop = Property(prop_id, prop_name, prop_dev_id, prop_values)

            self.prop_ids.append(prop_id)
            self.prop_names.append(prop_name)

            props.append(prop)

        super().__init__(props)

    def __contains__(self, item: int | str | Property) -> bool:
        if isinstance(item, int):
            return item in self.prop_ids
        elif isinstance(item, str):
            return item in self.prop_names
        elif isinstance(item, Property):
            return item in self.data
 