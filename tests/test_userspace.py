from src.py_xinput.userspace import *
from src.py_xinput.utils import get_command_output


def get_dev_ids(devs: list):
    return ' '.join([str(dev.id) for dev in devs])


class TestUserspace:
    def test_get_all_devices(self):
        all_devs = get_all_devices()
        
        all_dev_ids = [str(dev.id) for dev in all_devs if dev.master_id is not None]

        test_data = ' '.join(all_dev_ids)
        command = [
    'sh', '-c',
    "xinput list | grep -vE 'master' | grep -o 'id=[0-9]*' | cut -d= -f2 | tr '\n' ' '"
]
        actual_data = get_command_output(command).strip()

        assert test_data == actual_data

    def test_get_devices_by_master(self):
        all_devs = get_all_devices()

        master_devs = get_all_master_devices()

        for master_dev in master_devs:
            slave_dev_ids = [str(dev.id) for dev in all_devs if dev.master_id == master_dev.id]

            test_data = ' '.join(slave_dev_ids)
            command = [
        'sh', '-c', fr"xinput list | grep -E 'slave.*\({master_dev.id}\)' | grep -o 'id=[0-9]*' | cut -d= -f2 | tr '\n' ' '"
    ]
            actual_data = get_command_output(command).strip()

            assert test_data == actual_data
    
    # def test_
 

