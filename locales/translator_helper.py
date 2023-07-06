#!/usr/bin/env python3
from pathlib import Path
import json

# A little script to help fill in all the localization strings in the
# localization files.


def get_json_file(path):
    print(f"Reading from path {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_file(path, content):
    print(f"Writing to path {path}")
    path.write_text(json.dumps(content, ensure_ascii=False, indent=4))


def verify_localization_files(directory):
    directory = Path(directory)
    reference_file_path = directory / "en.json"
    reference_content = get_json_file(reference_file_path)

    for file_path in directory.iterdir():
        if file_path.name != "en.json" and file_path.name != "translator_helper.py":
            content = get_json_file(file_path)

            for key, value in reference_content.items():
                if key not in content:
                    print(f"Key {key} not found in {file_path.name}, adding it.")
                    # isinstance returns a boolean
                    if isinstance(value, list):
                        for item in value:
                            translated_value = input(
                                    f"Please enter a translation for '{item}'. (Member of list {value}): "
                            )
                    else:
                        translated_value = input(
                            f"Please enter a translation for '{value}':"
                        )
                    content[key] = translated_value

            write_json_file(file_path, content)


verify_localization_files("/home/rsp/programs/label_wires/locales/")
