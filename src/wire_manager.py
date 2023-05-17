#!/usr/bin/env python3
import datetime
import logging
import os
import re
import csv
from typing import List, Tuple
from abc import ABC, abstractmethod

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
    def __init__(self, csv_file_name, output_dir):
        self.csv_file_name = csv_file_name
        self.output_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), output_dir
        )
        self.wires = []

    def is_duplicate_or_reverse(self, wire) -> bool:
        reverse_wire = (wire[1], wire[0])
        return wire in self.wires or reverse_wire in self.wires

    def add_wire(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        dest_component: str,
        dest_terminal_block: str,
        dest_terminal: str,
    ):
        source_wire = (
            f"{source_component}-{source_terminal_block}-{source_terminal}".strip(
                "-"
            ).upper()
        )
        destination_wire = (
            f"{dest_component}-{dest_terminal_block}-{dest_terminal}".strip("-").upper()
        )
        wire = (source_wire, destination_wire)
        print(f"Adding wire: {wire}")
        if not self.is_duplicate_or_reverse(wire):
            self.wires.append(wire)
        else:
            print("Attempted to add duplicate or reverse wire.")

    @abstractmethod
    def save_to_csv(self) -> None:
        pass

    @abstractmethod
    def load_from_csv(self) -> None:
        pass


class GUIWireManager(WireManager):
    def __init__(self, csv_file_name, output_dir):
        super().__init__(csv_file_name, output_dir)

    def set_csv_file_name(self, csv_file_name):
        self.csv_file_name = csv_file_name

    def save_to_csv(self) -> None:
        file_path = self.csv_file_name

        try:
            os.makedirs(self.output_dir, exist_ok=True)

            with open(file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                for wire in self.wires:
                    csv_writer.writerow(wire)
            print(f"CSV file saved as {file_path}")
        except FileNotFoundError:
            print(f"Error: Directory '{self.output_dir}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to write to '{file_path}'.")
        except Exception as e:
            print(f"Error saving CSV file: {e}")

    def load_from_csv(self, selected_file: str) -> None:
        file_path = selected_file
        with open(file_path, "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                self.wires.append(tuple(row))
            print(
                f"Loaded {len(self.wires)} existing wire connections from {file_path}"
            )


class ConsoleWireManager(WireManager):
    def __init__(self, csv_file_name, output_dir) -> None:
        super().__init__(csv_file_name, output_dir)

    def is_duplicate_or_reverse(self, wire) -> bool:
        reverse_wire = (wire[1], wire[0])
        return wire in self.wires or reverse_wire in self.wires

    def print_wires(self) -> None:
        for i, wire in enumerate(self.wires):
            print(f"{i + 1}. {wire}")

    def gather_input(self) -> None:
        print(
            "Enter wire connection information. Leave fields empty to skip or skip component to quit."
        )
        while True:
            component = input("Component: ").upper()
            if component.lower() == "quit":
                print("Quitting...")
                break
            elif component.lower() == "print":
                self.print_wires()
                continue

            terminal_block = None
            while terminal_block != "":
                terminal_block = input(f"{component} + terminal block: ").upper()
                if not terminal_block:
                    print("Skipping...")
                    break

                if not is_valid_input(terminal_block):
                    print("Invalid terminal block. Please try again.")
                    continue

                terminal = None
                while terminal != "":
                    terminal = input(
                        f"{component}-{terminal_block} + terminal: "
                    ).upper()
                    if not terminal:
                        print("Skipping...")
                        break

                    if not is_valid_input(terminal):
                        print("Invalid terminal. Please try again.")
                        continue

                    destination = input(
                        f"{component}-{terminal_block}-{terminal}, destination: "
                    ).upper()

                    if not is_valid_destination(destination):
                        print("Invalid destination. Please try again.")
                        continue

                    wire = (f"{component}-{terminal_block}-{terminal}", destination)

                    if not self.is_duplicate_or_reverse(wire):
                        self.wires.append(wire)
                        print(
                            f"Added: {component}-{terminal_block}-{terminal}, {destination}"
                        )
                    else:
                        print("Duplicate or reverse duplicate detected. Skipping...")

    def save_to_csv(self) -> None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = f"{self.csv_file_name}_{timestamp}.csv"
        file_path = os.path.join(self.output_dir, file_name)

        try:
            os.makedirs(self.output_dir, exist_ok=True)

            with open(file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                self.print_wires()
                for wire in self.wires:
                    csv_writer.writerow(wire)
            print(f"CSV file saved as {file_name}")
        except FileNotFoundError:
            print(f"Error: Directory '{self.output_dir}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to write to '{file_path}'.")
        except Exception as e:
            print(f"Error saving CSV file: {e}")

    def load_from_csv(self) -> None:
        if not os.path.exists(self.output_dir):
            print(
                f"No existing files found in {self.output_dir}. Starting a new session"
            )

        matching_files = [
            file
            for file in os.listdir(self.output_dir)
            if file.startswith(f"{self.csv_file_name}_") and file.endswith(".csv")
        ]

        if not matching_files:
            print("No existing CSV files found. Starting a new session")
            return

        matching_files.sort(reverse=True)
        print("Matching CSV files:")
        for i, file in enumerate(matching_files):
            print(f"{i + 1}. {file}")

        selected_file_index = int(input("Enter the number of the file to load: ")) - 1
        if 0 <= selected_file_index < len(matching_files):
            file_path = os.path.join(
                self.output_dir, matching_files[selected_file_index]
            )
            with open(file_path, "r", newline="") as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    self.wires.append(tuple(row))
                print(
                    f"Loaded {len(self.wires)} existing wire connections from {file_path}:"
                )
                for i, wire in enumerate(self.wires):
                    print(f"{i + 1}. {wire}")
        else:
            print("No existing CSV file found. Starting a new session.")

    def filter_wires(self, filter_by, filter_value) -> List[Tuple[str, str]]:
        if filter_by not in ["component", "terminal_block", "terminal", "destination"]:
            print(f"Invalid filter option: {filter_by}")
            return []
        index_map = {
            "component": 0,
            "terminal_block": 1,
            "terminal": 2,
            "destination": 3,
        }
        filtered_wires = [
            wire
            for wire in self.wires
            if wire[0].split("-")[index_map[filter_by]].upper() == filter_value.upper()
        ]
        return filtered_wires
