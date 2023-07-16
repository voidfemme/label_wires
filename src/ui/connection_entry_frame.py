import tkinter as tk
from typing import TYPE_CHECKING

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
    def __init__(self, parent: MainView, controller: Controller, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

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
        self.lock_destination_checkbutton.grid(row=3, column=1, padx=5, pady=5)

    def create_and_place_buttons(self) -> None:
        self.undo_button = LocalizedButton(
            self, self.controller.localizer, "undo", command=self.on_undo_button_click
        )
        self.undo_button.grid(row=3, column=2, padx=5, pady=5)

        self.add_connection_button = LocalizedButton(
            self,
            self.controller.localizer,
            "add_connection",
            command=self.on_add_connection_button_click,
        )
        self.add_connection_button.grid(row=3, column=3, padx=5, pady=5)

    def define_bindings(self) -> None:
        # Define bindings
        self.source_component_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.source_terminal_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.destination_component_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
        )
        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.on_add_connection_button_click()
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
        self.controller.undo_connection_command()

    def increment(self, entry_widget: tk.Entry) -> None:
        # Alter to auto detect numbers along with letters, and update the number
        current_value = entry_widget.get()

        if current_value.isdigit():
            incremented_value = str(int(current_value) + 1)
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, incremented_value)
        else:
            self.parent.display_status(
                f"Error: The value in the entry box ({current_value}) is not a number"
            )
