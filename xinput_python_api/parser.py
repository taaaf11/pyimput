import subprocess

from .utils import get_command_output, slugify_label, clean_split

def get_mouse_devices_data():
    xinput_list_out_lines = get_command_output(['xinput', 'list']).decode().split('\n')
    pointer_count = 0
    pointer_started = False
    mouses_data = {}

    for output_line in xinput_list_out_lines: 
        if 'Virtual core pointer' in output_line:
            pointer_started = True
            master_id = clean_split(output_line.split())
            print(master_id)
        if 'XTEST' in output_line:
            continue

        pointer_count += 1
        line_split = clean_split(output_line.split())[:-3]

        dev_id = int(line_split[-1][3:])
        dev_name = ' '.join(line_split[:-1])

        dev_listing = get_command_output(['xinput', 'list', str(dev_id)]).decode().split('\n')

        # accidently got this algo
        supported_button_labels = dev_listing[4].split(':')[1].strip().split('"')
        supported_button_labels = [slugify_label(sup_label) for sup_label in supported_button_labels if sup_label.replace(' ', '').isalpha()]

        button_map = dict(list([(value, key) for key, value in enumerate(supported_button_labels, start=1)]))

        mouses_data.update({pointer_count: {'id': dev_id, 'device_name': dev_name, 'button_map': button_map}})
        return mouses_data

if __name__ == '__main__':
    print(get_mouse_devices_data())
