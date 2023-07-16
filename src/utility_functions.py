from enum import Enum, auto
import string

class ExportFormat(Enum):
    WIRE = auto()
    CABLE = auto()


def is_valid_entry_field_string(input_string: str) -> bool:
    # Check that input is a string
    if not isinstance(input_string, str):
        return False

    # Check for control characters
    if any(char not in string.printable for char in input_string):
        return False

    # If it passes both checks, it's a valid string.
    return True


def validate_json_wire_fields(input_data: list[dict[str, str]]) -> None:
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
