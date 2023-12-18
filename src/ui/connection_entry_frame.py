from importlib import resources
import json
import tkinter as tk
import re
from typing import TYPE_CHECKING
from pathlib import Path

from src.ui.localized_widgets import (
    LocalizedLabel,
    LocalizedButton,
    LocalizedCheckButton,
)
from src.connection import Connection

if TYPE_CHECKING:
    from src.controllers.controller import Controller
    from src.ui.main_view import MainView


class ConnectionEntryFrame(tk.Frame):
    def __init__(self, parent: "MainView", controller: "Controller", **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        current_script_path = Path(__file__)
        base_path = current_script_path.parents[2]

        bigram_frequency_path = base_path / "data" / "program_bigrams.json"

        # Before opening files
        print(f"Attempting to open bigram_frequency.json at: {bigram_frequency_path}")

        # Check if paths exist
        if not bigram_frequency_path.exists():
            print(f"bigram_frequency.json not found at {bigram_frequency_path}")

        with open(bigram_frequency_path, "r") as f:
            bigram_data = json.load(f)
        
        self.bigram_patterns = self.parse_bigram_data(bigram_data)

        # Define textvariables
        # Sources
        self.source_increment_toggle = tk.BooleanVar()
        self.source_component = tk.StringVar()
        self.source_terminal_block = tk.StringVar()
        self.source_terminal = tk.StringVar()

        # Destinations
        self.destination_increment_toggle = tk.BooleanVar()
        self.destination_component = tk.StringVar()
        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal = tk.StringVar()

        # Lock destination input to match what the user types in source input
        # In the future, update the text as the user types
        self.lock_destination_toggle = tk.BooleanVar()

        # Create and place widgets
        self.create_and_place_labels()
        self.create_and_place_entry_boxes()
        self.create_and_place_checkbuttons()
        self.create_and_place_buttons()
        self.define_bindings()

    def create_and_place_labels(self) -> None:
        self.component_label = LocalizedLabel(
            self, self.controller.localizer, "component"
        )
        self.component_label.grid(row=0, column=1, padx=5, pady=5)

        self.terminal_block_label = LocalizedLabel(
            self, self.controller.localizer, "terminal_block"
        )
        self.terminal_block_label.grid(row=0, column=2, padx=5, pady=5)

        self.terminal_label = LocalizedLabel(
            self, self.controller.localizer, "terminal"
        )
        self.terminal_label.grid(row=0, column=3, padx=5, pady=5)

        self.source_label = LocalizedLabel(self, self.controller.localizer, "field_one")
        self.source_label.grid(row=1, column=0, padx=5, pady=5)

        self.destination_label = LocalizedLabel(
            self, self.controller.localizer, "field_two"
        )
        self.destination_label.grid(row=2, column=0, padx=5, pady=5)

    def create_and_place_entry_boxes(self) -> None:
        self.source_component_entry = tk.Entry(self, textvariable=self.source_component)
        self.source_component_entry.grid(row=1, column=1, padx=5, pady=5)

        self.source_terminal_block_entry = tk.Entry(
            self, textvariable=self.source_terminal_block
        )
        self.source_terminal_block_entry.grid(row=1, column=2, padx=5, pady=5)

        self.source_terminal_entry = tk.Entry(self, textvariable=self.source_terminal)
        self.source_terminal_entry.grid(row=1, column=3, padx=5, pady=5)

        self.destination_component_entry = tk.Entry(
            self, textvariable=self.destination_component
        )
        self.destination_component_entry.grid(row=2, column=1, padx=5, pady=5)

        self.destination_terminal_block_entry = tk.Entry(
            self, textvariable=self.destination_terminal_block
        )
        self.destination_terminal_block_entry.grid(row=2, column=2, padx=5, pady=5)

        self.destination_terminal_entry = tk.Entry(
            self, textvariable=self.destination_terminal
        )
        self.destination_terminal_entry.grid(row=2, column=3)

    def create_and_place_checkbuttons(self) -> None:
        self.increment_source_checkbutton = LocalizedCheckButton(
            self,
            self.controller.localizer,
            "increment",
            variable=self.source_increment_toggle,
        )
        self.increment_source_checkbutton.grid(row=1, column=4, padx=5, pady=5)

        self.increment_destination_checkbutton = LocalizedCheckButton(
            self,
            self.controller.localizer,
            "increment",
            variable=self.destination_increment_toggle,
        )
        self.increment_destination_checkbutton.grid(row=2, column=4, padx=5, pady=5)

        self.lock_destination_checkbutton = LocalizedCheckButton(
            self,
            self.controller.localizer,
            "lock_destination",
            variable=self.lock_destination_toggle,
        )
        self.lock_destination_checkbutton.grid(row=3, column=4, padx=5, pady=5)

    def create_and_place_buttons(self) -> None:
        self.undo_button = LocalizedButton(
            self, self.controller.localizer, "undo", command=self.on_undo_button_click
        )
        self.undo_button.grid(row=3, column=1, padx=5, pady=5)

        self.redo_button = LocalizedButton(
            self, self.controller.localizer, "redo", command=self.on_redo_button_click
        )
        self.redo_button.grid(row=3, column=2, padx=5, pady=5)

        self.add_connection_button = LocalizedButton(
            self,
            self.controller.localizer,
            "add_connection",
            command=self.on_add_connection_button_click,
        )
        self.add_connection_button.grid(row=3, column=3, padx=5, pady=5)

    def toggle_destination(self) -> None:
        if self.lock_destination_toggle.get() is True:
            print("Setting toggle to False")
            self.lock_destination_toggle.set(False)
        elif self.lock_destination_toggle is False:
            print("Setting toggle to True")
            self.lock_destination_toggle.set(True)

    def define_bindings(self) -> None:
        # Define bindings
        self.source_component_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.source_component_entry.bind(
            "<Control-l>", lambda event: self.toggle_destination()
        )

        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.source_terminal_block_entry.bind(
            "<Control-l>", lambda event: self.toggle_destination()
        )

        self.source_terminal_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.source_terminal_entry.bind(
            "<Control-l>", lambda event: self.toggle_destination()
        )

        self.destination_component_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.destination_component_entry.bind(
            "<Control-l>", lambda event: self.toggle_destination()
        )

        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.destination_terminal_block_entry.bind(
            "<Control-l>", lambda event: self.toggle_destination()
        )

        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.destination_terminal_entry.bind(
            "<Control-l>", lambda event: self.toggle_destination()
        )

    def populate_entries(self, connection: Connection) -> None:
        self.source_component.set(connection.source_component)
        self.source_terminal_block.set(connection.source_terminal_block)
        self.source_terminal.set(connection.source_terminal)

        self.destination_component.set(connection.destination_component)
        self.destination_terminal_block.set(connection.destination_terminal_block)
        self.destination_terminal.set(connection.destination_terminal)

    def on_add_connection_button_click(self) -> None:
        # Get user input from the UI
        source = {
            "component": self.source_component.get(),
            "terminal_block": self.source_terminal_block.get(),
            "terminal": self.source_terminal.get(),
        }

        if self.lock_destination_toggle.get():
            # Set destination fields to match source fields
            self.destination_component.set(source["component"])
            self.destination_terminal_block.set(source["terminal_block"])
            self.destination_terminal.set(source["terminal"])

        destination = {
            "component": self.destination_component.get(),
            "terminal_block": self.destination_terminal_block.get(),
            "terminal": self.destination_terminal.get(),
        }

        # Do not add the wire if the fields are empty.
        if self.is_empty_label(
            source["component"],
            source["terminal_block"],
            source["terminal"],
            destination["component"],
            destination["terminal_block"],
            destination["terminal"],
        ):
            return

        self.controller.add_connection_command(source, destination)

        if self.source_increment_toggle.get():
            self.increment(self.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.increment(self.destination_terminal_entry)
        self.parent.scroll_to_bottom_of_treewidget()

    def is_empty_label(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ) -> bool:
        return (
            source_component == ""
            and source_terminal_block == ""
            and source_terminal == ""
            and destination_component == ""
            and destination_terminal_block == ""
            and destination_terminal == ""
        )

    def on_undo_button_click(self) -> None:
        print("Undo button clicked!")
        self.controller.undo_connection_command()

    def on_redo_button_click(self) -> None:
        print("Redo button clicked!")
        self.controller.redo_connection_command()

    def increment(self, entry_widget: tk.Entry) -> None:
        current_value = entry_widget.get()

        # Check if the current value matches a known pattern
        if current_value in self.bigram_patterns:
            incremented_value = self.bigram_patterns[current_value]
        else:
            # If it doesn't match a pattern, perform a regular increment
            incremented_value = self.increment_string_value(current_value)

        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, incremented_value)

    def parse_bigram_data(self, bigram_data: dict) -> dict:
        """
        Convert the bigram data from string format to a usable format. (e.g. tuples).
        """
        parsed_data = {}
        for bigram, count in bigram_data.items():
            source, destination = bigram.split("->")
            parsed_data[(source, destination)] = count
        return parsed_data

    def increment_string_value(self, s: str) -> str:
        # Check for range pattern (e.g., "2-9")
        range_match = re.match(r"(\d+)-(\d+)", s)
        if range_match:
            start, end = map(int, range_match.groups())
            increment = end - start
            return f"{start + increment + 1}-{end + increment + 1}"

        # If no range, increment numerically or alphanumerically
        numbers = re.findall(r"\d+", s)
        if numbers:
            last_number = numbers[-1]
            incremented_number = str(int(last_number) + 1)
            incremented_string = s[::-1].replace(
                last_number[::-1], incremented_number[::-1], 1
            )[::-1]
            return incremented_string
        else:
            return s  # Return the original string if no numbers are found
