import tkinter as tk
from tkinter import ttk

from src.localized_widgets import LocalizedLabel, LocalizedButton, LocalizedCheckButton


class ConnectionEntryFrame(tk.Frame):
    def __init__(
        self, parent, localizer, settings, connection_manager, command_manager, **kwargs
    ):
        super().__init__(parent)
        self.parent = parent
        self.localizer = localizer
        self.settings = settings
        self.connection_manager = connection_manager
        self.command_manager = command_manager

        # Create and place widgets
        self.create_and_place_labels()
        self.create_and_place_entry_boxes()
        self.create_and_place_checkbuttons()
        self.create_and_place_buttons()
        self.define_bindings()

        self.horizontal_rule = ttk.Separator(self, orient="horizontal")
        self.horizontal_rule.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)

    def create_and_place_labels(self):
        self.component_label = LocalizedLabel(self, self.localizer, "component")
        self.component_label.grid(row=0, column=1, padx=5, pady=5)

        self.terminal_block_label = LocalizedLabel(
            self, self.localizer, "terminal_block"
        )
        self.terminal_block_label.grid(row=0, column=2, padx=5, pady=5)

        self.terminal_label = LocalizedLabel(self, self.localizer, "terminal")
        self.terminal_label.grid(row=0, column=3, padx=5, pady=5)

        self.source_label = LocalizedLabel(self, self.localizer, "field_one")
        self.source_label.grid(row=1, column=0, padx=5, pady=5)

        self.destination_label = LocalizedLabel(self, self.localizer, "field_two")
        self.destination_label.grid(row=2, column=0, padx=5, pady=5)

    def create_and_place_entry_boxes(self):
        self.source_component_entry = tk.Entry(
            self, textvariable=self.get_parent_attribute("source_component")
        )
        self.source_component_entry.grid(row=1, column=1, padx=5, pady=5)

        self.source_terminal_block_entry = tk.Entry(
            self, textvariable=self.get_parent_attribute("source_terminal_block")
        )
        self.source_terminal_block_entry.grid(row=1, column=2, padx=5, pady=5)

        self.source_terminal_entry = tk.Entry(
            self, textvariable=self.get_parent_attribute("source_terminal")
        )
        self.source_terminal_entry.grid(row=1, column=3, padx=5, pady=5)

        self.destination_component_entry = tk.Entry(
            self, textvariable=self.get_parent_attribute("destination_component")
        )
        self.destination_component_entry.grid(row=2, column=1, padx=5, pady=5)

        self.destination_terminal_block_entry = tk.Entry(
            self, textvariable=self.get_parent_attribute("destination_terminal_block")
        )
        self.destination_terminal_block_entry.grid(row=2, column=2, padx=5, pady=5)

        self.destination_terminal_entry = tk.Entry(
            self, textvariable=self.get_parent_attribute("destination_terminal")
        )
        self.destination_terminal_entry.grid(row=2, column=3)

    def create_and_place_checkbuttons(self):
        self.increment_source_checkbutton = LocalizedCheckButton(
            self,
            self.localizer,
            "increment",
            variable=self.get_parent_attribute("source_increment_toggle"),
        )
        self.increment_source_checkbutton.grid(row=1, column=4, padx=5, pady=5)

        self.increment_destination_checkbutton = LocalizedCheckButton(
            self,
            self.localizer,
            "increment",
            variable=self.get_parent_attribute("destination_increment_toggle"),
        )
        self.increment_destination_checkbutton.grid(row=2, column=4, padx=5, pady=5)

        self.lock_destination_checkbutton = LocalizedCheckButton(
            self,
            self.localizer,
            "lock_destination",
            variable=self.get_parent_attribute("lock_destination_toggle"),
        )
        self.lock_destination_checkbutton.grid(row=3, column=1, padx=5, pady=5)

    def create_and_place_buttons(self):
        self.undo_button = LocalizedButton(
            self, self.localizer, "undo", command=self.parent.undo
        )
        self.undo_button.grid(row=3, column=2, padx=5, pady=5)

        self.add_connection_button = LocalizedButton(
            self,
            self.localizer,
            "add_connection",
            command=self.parent.add_connection
        )
        self.add_connection_button.grid(row=3, column=3, padx=5, pady=5)

    def define_bindings(self) -> None:
        # Define bindings
        self.source_component_entry.bind(
            "<Return>", lambda event: self.parent.add_connection()
        )
        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.parent.add_connection()
        )
        self.source_terminal_entry.bind(
            "<Return>", lambda event: self.parent.add_connection()
        )
        self.destination_component_entry.bind(
            "<Return>", lambda event: self.parent.add_connection()
        )
        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.parent.add_connection()
        )
        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.parent.add_connection()
        )

    def call_parent_method(self, method_name, *args, **kwargs):
        method = getattr(self.parent, method_name, None)
        if method:
            return method(*args, **kwargs)
        else:
            raise AttributeError(f"No such method: {method_name}")

    def get_parent_attribute(self, attribute_name):
        attribute = getattr(self.parent, attribute_name, None)
        if attribute is None:
            raise AttributeError(f"No such attribute: {attribute_name}")
        return attribute
