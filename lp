# Workers of the world, Unite!
import json
import os
import tkinter as tk
from tkinter import ttk
from src.wire_manager import is_valid_file_name
from src.settings_window import SettingsWindow


class WireApp(tk.Tk):
    def __init__(self, wire_manager, file_name: str):
        super().__init__()

        self.title("Wire Manager")
        self.wires_list = []
        self.wires_dict = {}
        self.tree_item_to_wire = {}
        self.selected_wires = []

        # json file name
        self.data_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "src", "data"
        )
        abs_file_path = os.path.join(self.data_dir, file_name)
        self.json_file_name = tk.StringVar(value=abs_file_path)

        self.wire_manager = wire_manager

        # Cable mode
        self.cable_mode_toggle = tk.BooleanVar()
        self.lock_destination_toggle = tk.BooleanVar()
        print("Initialized Cable Mode")

        # Sources
        self.source_increment_toggle = tk.BooleanVar()
        self.source_component = tk.StringVar()
        self.source_terminal_block = tk.StringVar()
        self.source_terminal = tk.StringVar()
        print("Initialized Sources")

        # Destinations
        self.destination_increment_toggle = tk.BooleanVar()
        self.destination_component = tk.StringVar()
        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal = tk.StringVar()
        print("Initialized destination")

        self.create_widgets()
        self.load_wires()
        print("Finished Initializing WireApp")

    def create_widgets(self):
        # Define labels
        self.file_name_field = tk.Label(self, textvariable=self.json_file_name)
        self.component_label = tk.Label(self, text="Component")
        self.terminal_block_label = tk.Label(self, text="Terminal Block")
        self.terminal_label = tk.Label(self, text="Terminal")
        self.file_name_field_label = tk.Label(self, text="Saving as:")
        self.source_label = tk.Label(self, text="P1:")
        self.destination_label = tk.Label(self, text="P2:")
        self.status_label = tk.Label(self, text="")

        # Define Entry fields
        self.file_name_field = tk.Entry(self, textvariable=self.json_file_name)
        self.source_component_entry = tk.Entry(self, textvariable=self.source_component)
        self.source_terminal_block_entry = tk.Entry(
            self, textvariable=self.source_terminal_block
        )
        self.source_terminal_entry = tk.Entry(self, textvariable=self.source_terminal)

        self.destination_component_entry = tk.Entry(
            self, textvariable=self.destination_component
        )
        self.destination_terminal_block_entry = tk.Entry(
            self, textvariable=self.destination_terminal_block
        )
        self.destination_terminal_entry = tk.Entry(
            self, textvariable=self.destination_terminal
        )

        # Define Checkbuttons
        self.source_increment_checkbutton = tk.Checkbutton(
            self, text="Increment", variable=self.source_increment_toggle
        )
        self.destination_increment_checkbutton = tk.Checkbutton(
            self, text="Increment", variable=self.destination_increment_toggle
        )
        self.cable_mode_checkbutton = tk.Checkbutton(
            self, text="Cable Mode", variable=self.cable_mode_toggle
        )
        self.lock_destination_checkbutton = tk.Checkbutton(
            self, text="Lock Destination", variable=self.lock_destination_toggle
        )

        # Define buttons
        self.save_button = tk.Button(self, text="Save File", command=self.save_file)
        self.add_wire_button = tk.Button(self, text="Add Wire", command=self.add_wire)
        self.settings_button = tk.Button(
            self, text="Settings", command=self.open_settings_window
        )
        self.delete_button = tk.Button(
            self, text="Delete Wire", command=self.delete_wire
        )

        # Define bindings
        self.source_component_entry.bind("<Return>", lambda event: self.add_wire())
        self.source_terminal_block_entry.bind("<Return>", lambda event: self.add_wire())
        self.source_terminal_entry.bind("<Return>", lambda event: self.add_wire())
        self.destination_component_entry.bind("<Return>", lambda event: self.add_wire())
        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.add_wire()
        )
        self.destination_terminal_entry.bind("<Return>", lambda event: self.add_wire())
        self.file_name_field.bind("<Return>", lambda event: self.save_file())

        # Define text area for wire numbers
        # self.wire_list = tk.Listbox(self, selectmode=tk.EXTENDED)
        self.tree_widget = self.create_tree_widget()

        # Arrange widgets in grid (left to right, top to bottom)
        self.tree_widget.grid(row=1, column=0, rowspan=6, padx=5, pady=5)
        self.file_name_field_label.grid(row=1, column=1, padx=5, pady=5)
        self.file_name_field.grid(
            row=1, column=2, columnspan=3, sticky="ew", padx=5, pady=5
        )
        self.cable_mode_checkbutton.grid(row=2, column=4, padx=5, pady=5)
        self.lock_destination_checkbutton.grid(row=2, column=5, padx=5, pady=5)

        self.component_label.grid(row=3, column=2, padx=5, pady=5)
        self.terminal_block_label.grid(row=3, column=3, padx=5, pady=5)
        self.terminal_label.grid(row=3, column=4, padx=5, pady=5)

        self.source_label.grid(row=5, column=1, padx=5, pady=5)
        self.source_component_entry.grid(row=5, column=2, padx=5, pady=5)
        self.source_terminal_block_entry.grid(row=5, column=3, padx=5, pady=5)
        self.source_terminal_entry.grid(row=5, column=4, padx=5, pady=5)
        self.source_increment_checkbutton.grid(row=5, column=5, padx=5, pady=5)

        self.destination_label.grid(row=6, column=1, padx=5, pady=5)
        self.destination_component_entry.grid(row=6, column=2, padx=5, pady=5)
        self.destination_terminal_block_entry.grid(row=6, column=3, padx=5, pady=5)
        self.destination_terminal_entry.grid(row=6, column=4, padx=5, pady=5)
        self.destination_increment_checkbutton.grid(row=6, column=5, padx=5, pady=5)
        self.add_wire_button.grid(row=7, column=2, padx=5, pady=5)
        self.settings_button.grid(row=7, column=5, padx=5, pady=5)

        self.delete_button.grid(row=7, column=0, padx=5, pady=5)
        self.save_button.grid(row=8, column=0, padx=5, pady=5)

        self.status_label.grid(
            row=9, column=0, columnspan=5, sticky="w", padx=5, pady=5
        )
        self.update_wire_list()

    def create_tree_widget(self):
        columns = ("Source", "Destination")
        tree = ttk.Treeview(self, columns=columns, show="headings")

        # Define headings
        tree.heading("Source", text="Source")
        tree.heading("Destination", text="Destination")

        tree.bind("<<TreeviewSelect>>", self.update_selected_wires)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree["yscrollcommand"] = scrollbar.set  # Link the scrollbar to the treeview

        return tree

    def update_selected_wires(self, event):
        print(f"event = {event}")

        # Get currently selected items
        selected_items = self.tree_widget.selection()
        print(f"selected_items: {selected_items}")

        # Clear the selected wires list
        self.selected_wires = []

        # Add all currently selected wires to the list
        for item in selected_items:
            wire = self.tree_item_to_wire.get(item)
            if wire:
                self.selected_wires.append(wire)
                print(f"selected_wires: {self.selected_wires}")

        print(f"self.selected_wires = {self.selected_wires}")

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)

    def validate_json_content(self, content):
        try:
            json.loads(content)
        except json.JSONDecodeError:
            return False
        return True

    def increment(self, input_box: tk.Entry):
        try:
            value = int(input_box.get())
            input_box.delete(0, tk.END)
            input_box.insert(0, str(value + 1))
        except ValueError:
            self.status_label[
                "text"
            ] = "Warning: Terminal value not numeric. Wire added without incrementing."

    def is_empty_label(
        self,
        source_component,
        source_terminal_block,
        source_terminal,
        destination_component,
        destination_terminal_block,
        destination_terminal,
    ) -> bool:
        wire = Wire(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        if wire.is_empty():
            self.status_label["text"] = "Attempted to add an empty wire."
            return True
        return False

    def add_wire(self):
        source_component = self.source_component.get()
        source_terminal_block = self.source_terminal_block.get()
        source_terminal = self.source_terminal.get()

        if self.lock_destination_toggle.get():
            # Set destination fields to match source fields
            self.destination_component.set(source_component)
            self.destination_terminal_block.set(source_terminal_block)
            self.destination_terminal.set(source_terminal)

        destination_component = self.destination_component.get()
        destination_terminal_block = self.destination_terminal_block.get()
        destination_terminal = self.destination_terminal.get()

        # Check if every field is empty
        if self.is_empty_label(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        ):
            return

        wire = self.wire_manager.add_wire(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        # Add to tree widget and get unique identifier
        item = self.tree_widget.insert(
            "",
            "end",
            values=(
                f"{source_component}-{source_terminal_block}-{source_terminal}",
                f"{destination_component}-{destination_terminal_block}-{destination_terminal}",
            ),
        )

        # Add to the mapping dictionary
        self.tree_item_to_wire[item] = wire

        # Update the listbox to reflect the new wire list
        self.update_wire_list()

        if self.source_increment_toggle.get():
            self.increment(self.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.increment(self.destination_terminal_entry)

    def delete_wire(self):
        print("delete")
        for item in self.tree_widget.selection():
            wire = self.tree_item_to_wire[item]
            print(f"Deleting wire: {wire}")
            self.wire_manager.delete_wire(wire)
            del self.wires_dict[str(wire)]
            del self.tree_item_to_wire[item]
        self.update_wire_list()
        self.selected_wires = []

    def populate_wires(self):
        self.wire_manager.load_from_file()
        for wire in self.wire_manager.get_wires():
            wire_str = str(wire)
            self.wires_dict[wire_str] = wire
            self.tree_widget.insert("", "end", text=wire_str)

    def update_wire_list(self):
        # First, clear all existing items in the Treeview
        for i in self.tree_widget.get_children():
            self.tree_widget.delete(i)

        # Then, add all the wires currently in the WireManager
        for wire in self.wire_manager.get_wires():
            source = f"{wire.source_component}-{wire.source_terminal_block}-{wire.source_terminal}".strip(
                "-"
            ).replace(
                "--", "-"
            )
            destination = f"{wire.destination_component}-{wire.destination_terminal_block}-{wire.destination_terminal}".strip(
                "-"
            ).replace(
                "--", "-"
            )
            self.tree_widget.insert("", "end", text="", values=(source, destination))

    def run_program(self):
        print("Running program")
        json_file_name = self.json_file_name.get()
        if is_valid_file_name(json_file_name):
            print("Is valid file name")
            self.wire_manager.set_json_file_name(json_file_name)
            self.wire_manager.load_from_file()
            self.update_wire_list()
        print("Invalid file name")

    def save_file(self) -> None:
        pass

    def load_wires(self):
        self.wire_manager.load_from_file()
        self.update_wire_list()

    def export_to_csv(self) -> None:
        pass
