import subprocess
from typing import List, Sequence
from string import ascii_lowercase, digits

from type import PropsDict


def get_command_output(command: list):
    return subprocess.run(command, capture_output=True).stdout.decode()


run_command = subprocess.run


# not exactly a slug, but for naming ¯\_(ツ)_/¯
def slugify_label(label: str) -> str:
    slugified_label = label.lower().replace(" ", "_")
    return slugified_label


def clean_split(line_split: Sequence[str]) -> List[str]:
    useless_chars = "⎡⎜⎣↳∼"
    return [word for word in line_split if word not in useless_chars]


def get_prop_details_from_prop_line(dev_id: int, prop_line: str) -> PropsDict:
    prop_details = {}
    prop_line_split = prop_line.split()
    for word in prop_line_split:
        if (
            word.startswith("(")
            and word.endswith(":")
            and word.strip("(:)").isnumeric()
        ):
            index_of_property: int = prop_line_split.index(word)

            prop_id = int(word.strip("(:)"))
            prop_name = "_".join(prop_line_split[:index_of_property]).lower()
            prop_values = " ".join(prop_line_split[(index_of_property + 1) :]).split(
                ","
            )
            prop_values = [prop_value.strip() for prop_value in prop_values]

            prop_details.update(
                {
                    prop_name: {
                        "dev_id": dev_id,
                        "prop_id": prop_id,
                        "prop_name": prop_name,
                        "values": prop_values,
                    }
                }
            )

    return prop_details


def get_keys_with_types() -> dict:
    keysyms = {}

    specials = ["minus", "equal", "bracketleft", "bracketright", "semicolon", "apostrophe", "comma", "period", "slash", "grave", "backslash"]
    
    keycodes_output = get_command_output(["sh", "-c", "xmodmap -pke"]).split('\n')[:-1]

    for line in keycodes_output:
        split = line.split()
        keycode, values = int(split[1]), split[3:]

        # this variable signifies whether the "normal" and Shift variants of the
        # key are similar, as in "q" and "Q".
        # It also shows whether the Shift variant is "NoSymbol".
        is_similar = False

        if len(values) == 0:
            continue

        if values[0] == values[1].lower() or values[1] == 'NoSymbol':
            is_similar = True

        if values[0] in ascii_lowercase:
            alphabets = keysyms.get('alphabets') or {}
            if is_similar:
                alphabets.update({keycode: values[0].capitalize()})
            else:
                alphabets.update({keycode: " ".join(values[:2]).title()})

            keysyms.update({'alphabets': alphabets})

        elif values[0] in digits:
            numbers = keysyms.get('numbers') or {}
            if is_similar:
                numbers.update({keycode: values[0].capitalize()})
            else:
                numbers.update({keycode: " ".join(values[:2]).title()})

            keysyms.update({'numbers': numbers})

        elif values[0] in specials:
            special = keysyms.get('special') or {}
            if is_similar:
                special.update({keycode: values[0].capitalize()})
            else:
                special.update({keycode: " ".join(values[:2]).title()})

            keysyms.update({'special': special})


    return keysyms


def get_keysyms_enumeration(keysyms_dict: dict) -> dict:
    sorted_keys = sorted(keysyms_dict.keys())
    values = []
    for s_key in sorted_keys:
        for keycode, keysym in keysyms_dict[s_key].items():
            values.append((keycode, keysym))

    return dict(enumerate(values, start=1))

