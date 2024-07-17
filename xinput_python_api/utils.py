import subprocess

def get_command_output(command: list):
    return subprocess.run(command, capture_output=True).stdout

def slugify_label(label: str):
    slugified_label = label.lower().replace(' ', '_')
    return slugified_label

def clean_split(line_split: list[str]):
    useless_chars = '⎡⎜⎣↳'
    return [word for word in line_split if word not in useless_chars]
