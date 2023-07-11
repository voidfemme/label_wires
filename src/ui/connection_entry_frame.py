import tkinter as tk
from tkinter import ttk

from src.localized_widgets import LocalizedLabel, LocalizedButton, LocalizedCheckButton
from src.command import AddConnectionCommand


class ConnectionEntryFrame(tk.Frame):
    def __init__(
        self,
        parent,
        localizer,
        settings,
        connection_manager,
        command_manager,
        event_system,
        **kwargs
    ):
        super().__init__(parent)
        self.parent = parent
        self.localizer = localizer
        self.settings = settings
        self.connection_manager = connection_manager
        self.command_manager = command_manager
        self.event_system = event_system

        self.business_logic = ConnectionEntryFrameBusinessLogic(self)

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
        # Perhaps do this live in the near future
        self.lock_destination_toggle = tk.BooleanVar()

        # Create and place widgets
        self.create_and_place_labels()
        self.create_and_place_entry_boxes()
        self.create_and_place_checkbuttons()
        self.create_and_place_buttons()
        self.define_bindings()

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

    def create_and_place_checkbuttons(self):
        self.increment_source_checkbutton = LocalizedCheckButton(
            self, self.localizer, "increment", variable=self.source_increment_toggle
        )
        self.increment_source_checkbutton.grid(row=1, column=4, padx=5, pady=5)

        self.increment_destination_checkbutton = LocalizedCheckButton(
            self,
            self.localizer,
            "increment",
            variable=self.destination_increment_toggle,
        )
        self.increment_destination_checkbutton.grid(row=2, column=4, padx=5, pady=5)

        self.lock_destination_checkbutton = LocalizedCheckButton(
            self,
            self.localizer,
            "lock_destination",
            variable=self.lock_destination_toggle,
        )
        self.lock_destination_checkbutton.grid(row=3, column=1, padx=5, pady=5)

    def create_and_place_buttons(self):
        self.undo_button = LocalizedButton(
            self, self.localizer, "undo", command=self.undo
        )
        self.undo_button.grid(row=3, column=2, padx=5, pady=5)

        self.add_connection_button = LocalizedButton(
            self, self.localizer, "add_connection", command=self.add_connection
        )
        self.add_connection_button.grid(row=3, column=3, padx=5, pady=5)

    def define_bindings(self) -> None:
        # Define bindings
        self.source_component_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.source_terminal_entry.bind("<Return>", lambda event: self.add_connection())
        self.destination_component_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )

    def add_connection(self) -> None:
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

        # Check if every field is empty
        if self.is_empty_label(
            source["component"],
            source["terminal_block"],
            source["terminal"],
            destination["component"],
            destination["terminal_block"],
            destination["terminal"],
        ):
            return

        self.business_logic.add_connection(source, destination)

        if self.source_increment_toggle.get():
            self.parent.increment(self.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.parent.increment(self.destination_terminal_entry)
        self.parent.scroll_to_bottom_of_treewidget()

    def is_empty_label(
        self,
        source_component,
        source_terminal_block,
        source_terminal,
        destination_component,
        destination_terminal_block,
        destination_terminal,
    ) -> bool:
        return (
            source_component == ""
            and source_terminal_block == ""
            and source_terminal == ""
            and destination_component == ""
            and destination_terminal_block == ""
            and destination_terminal == ""
        )

    def undo(self) -> None:
        if self.command_manager.undo_stack:
            command = self.command_manager.undo_stack.pop()
            command.undo()


class ConnectionEntryFrameBusinessLogic:
    def __init__(self, parent):
        self.parent = parent

    def add_connection(self, source, destination) -> None:
        cmd = AddConnectionCommand(
            self.parent.event_system,
            self.parent.connection_manager,
            source,
            destination,
        )
        self.parent.command_manager.execute(cmd)
