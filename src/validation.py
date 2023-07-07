from pathlib import Path
import os
import re
import string


def is_valid_file_path(path: str) -> bool:
    file_path = Path(path)
    dir_name = file_path.parent
    file_name = file_path.name

    if os.name == "nt":  # For Windows systems
        valid_path_chars = not bool(re.search(r'[<>:"|?*]|\.$|\s$', file_name))
    else:  # For Unix/Linux based systems
        valid_path_chars = "\0" not in path

    # Check if path exists and if it has write Permissions
    path_exists = dir_name.exists()
    can_write = os.access(dir_name, os.W_OK)

    # Check in connection_manager.py for logic pertaining to '.wire' and '.cable'
    # suffixes

    if not path_exists:
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not can_write:
        raise PermissionError(f"No write permissions for path: {path}")

    return valid_path_chars


def is_valid_entry_string(input_string) -> bool:
    # Check that input is a string
    if not isinstance(input_string, str):
        return False

    # Check for control characters
    if any(char not in string.printable for char in input_string):
        return False

    # If it passes both checks, it's a valid string.
    return True


def validate_json_data(input_data: dict) -> None:
    required_fields = [
        "source_component",
        "source_terminal_block",
        "source_terminal",
        "destination_component",
        "destination_terminal_block",
        "destination_terminal",
    ]

    if not isinstance(input_data, list):
        raise ValueError("Invalid data: root element should be a list.")

    for item in input_data:
        if not isinstance(item, dict):
            raise ValueError(
                "Invalid data: all elements in list should be dictionaries."
            )

        for field in required_fields:
            if field not in item:
                raise ValueError(f"Invalid data: missing '{field}'.")
            if not isinstance(item[field], str):
                raise ValueError(f"Invalid data: '{field}' should be a string.")
