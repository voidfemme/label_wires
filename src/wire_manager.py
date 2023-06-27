import json
import logging
import os
import re
from abc import ABC, abstractmethod
from src.wire import Wire

# Global variable for the directory path
WIRENUMS_DIR = "data"

# Basic configuration for the logging system
logging.basicConfig(filename="app.log", level=logging.DEBUG)


def is_valid_input(input_string) -> bool:
    # Check if the input is alphanumeric
    return input_string.isalnum()


def is_valid_destination(destination) -> bool:
    pattern = re.compile(r"^\w+(-\w+){1,3}$")
    return bool(pattern.match(destination))


def is_valid_file_name(file_name) -> bool:
    # Check for invalid characters in the file name
    invalid_characters = {"<", ">", ":", '"', "\\", "/", "|", "?", "*"}
    return not any(char in file_name for char in invalid_characters)


class WireManager(ABC):
    def __init__(self, file_name, output_dir):
        self.file_name = file_name
        self.output_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), output_dir
        )
        self.wires = []

    @abstractmethod
    def save_to_file(self, content) -> bool:
        pass


class GUIWireManager(WireManager):
    def __init__(self, file_name, output_dir):
        super().__init__(file_name, output_dir)

    def set_json_file_name(self, file_name):
        self.file_name = file_name

    def save_to_file(self) -> bool:
        abs_file_path = self.file_name
        try:
            with open(abs_file_path, "w") as file:
                json.dump([wire.to_dict() for wire in self.wires], file)
            return True
        except FileNotFoundError:
            return False

    def load_from_file(self) -> None:
        file_path = os.path.join(self.output_dir, self.file_name)
        print(file_path)

        try:
            with open(file_path, "r") as json_file:
                wire_dicts = json.load(json_file)
            self.wires = [
                Wire(**wire_dict)
                for wire_dict in wire_dicts
                if not Wire(**wire_dict).is_empty()
            ]
            # Print each wire loaded
            for wire in self.wires:
                print(f"Loaded wire: {wire}")
            print(f"JSON file loaded as {file_path}")
        except FileNotFoundError:
            print(f"Error: Directory '{self.output_dir}' not found")
        except PermissionError:
            print(f"Error: Permission denied to read from'{file_path}'")
        except Exception as e:
            print(f"Error loading JSON file: {e}")

    def delete_wire(self, wire_to_delete):
        if wire_to_delete in self.wires:
            self.wires.remove(wire_to_delete)
            self.save_to_file()
        else:
            print("Attempted to delete a wire that doesn't exist.")

    def edit_wire(self, old_wire: Wire, new_wire: Wire):
        if old_wire in self.wires:
            # If new wire already exists or is the reverse of an existing wire, don't do the edit
            if new_wire in self.wires:
                print(
                    "Attempted to edit wire into a duplicate or reverse duplicate wire."
                )
                return False
            # Find the index of the old wire and replace it with the new one
            index = self.wires.index(old_wire)
            self.wires[index] = new_wire
            # Save updated wires to file
            self.save_to_file()
            return True
        else:
            print("Attempted to edit a wire that doesn't exist.")
            return False

    def add_wire(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ):
        wire = Wire(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )
        print(f"Adding wire: {wire}")
        if wire not in self.wires:
            self.wires.append(wire)
            # Converting wires to dict before saving to file
            self.save_to_file()
        else:
            print("Attempted to add duplicate or reverse wire.")

    def get_wires(self):
        return self.wires
