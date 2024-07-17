import subprocess


class XInputDevice:
    def __init__(self, device_data: dict):
        self.id = device_data['id']
        self.master_id = device_data['master_id']
        self.name = device_data['device_name']
        self.props = device_data['props']

    def list_props(self):
        print(self.props)


#    def enable(self, ...):
        
#        ...

#    def disable(self, ...):
#        ...
