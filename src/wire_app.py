#!/usr/bin/env python3
# Workers of the world, Unite!

import csv
import io
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext
from src.wire_manager import GUIWireManager, WIRENUMS_DIR, is_valid_file_name
from src.settings_window import SettingsWindow


class WireApp(tk.Tk):
    def __init__(self, file_name: str):
        super().__init__()

        self.title("Wire Manager")

        # csv file name
        self.data_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "src", "data"
        )
        print(f"WireApp.data_dir: {self.data_dir}")
        abs_file_path = os.path.join(self.data_dir, file_name)
        print(f"WireApp abs_file_path: {abs_file_path}")
        self.csv_file_name = tk.StringVar(value=abs_file_path)

        self.wire_manager = GUIWireManager(self.csv_file_name.get(), WIRENUMS_DIR)

        # Cable mode
        self.cable_mode_toggle = tk.BooleanVar()
        self.lock_destination_toggle = tk.BooleanVar()

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

        self.counter = 0
        self.label1 = tk.Label(self)
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.create_widgets()
        self.load_wires()

    def capitalize_scrolledtext(self):
        content = self.wire_list.get("1.0", "end-1c")
        capitalized_content = content.upper()
        self.wire_list.delete("1.0", tk.END)
        self.wire_list.insert("1.0", capitalized_content)

    def create_widgets(self):
        # Define labels
        self.label1 = tk.Label(self, textvariable=self.csv_file_name)
        self.component_label = tk.Label(self, text="Component")
        self.terminal_block_label = tk.Label(self, text="Terminal Block")
        self.terminal_label = tk.Label(self, text="Terminal")
        self.file_name_field_label = tk.Label(self, text="Saving as:")
        self.source_label = tk.Label(self, text="Source ->")
        self.destination_label = tk.Label(self, text="Destination ->")
        self.status_label = tk.Label(self, text="")

        # Define Entry fields
        self.file_name_field = tk.Entry(self, textvariable=self.csv_file_name)
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
        self.wire_list = scrolledtext.ScrolledText(self, width=30, height=15)

        # Arrange widgets in grid (left to right, top to bottom)
        self.wire_list.grid(row=1, column=0, rowspan=6, padx=10, pady=10)
        self.file_name_field_label.grid(row=1, column=1, padx=10, pady=10)
        self.file_name_field.grid(
            row=1, column=2, columnspan=3, sticky="ew", padx=10, pady=10
        )

        self.component_label.grid(row=3, column=2, padx=10, pady=10)
        self.terminal_block_label.grid(row=3, column=3, padx=10, pady=10)
        self.terminal_label.grid(row=3, column=4, padx=10, pady=10)

        self.save_button.grid(row=7, column=0, padx=10, pady=10)

        self.source_label.grid(row=5, column=1, padx=10, pady=10)
        self.source_component_entry.grid(row=5, column=2, padx=10, pady=10)
        self.source_terminal_block_entry.grid(row=5, column=3, padx=10, pady=10)
        self.source_terminal_entry.grid(row=5, column=4, padx=10, pady=10)
        self.source_increment_checkbutton.grid(row=5, column=5, padx=10, pady=10)

        self.destination_label.grid(row=6, column=1, padx=10, pady=10)
        self.destination_component_entry.grid(row=6, column=2, padx=10, pady=10)
        self.destination_terminal_block_entry.grid(row=6, column=3, padx=10, pady=10)
        self.destination_terminal_entry.grid(row=6, column=4, padx=10, pady=10)
        self.destination_increment_checkbutton.grid(row=6, column=5, padx=10, pady=10)

        self.cable_mode_checkbutton.grid(row=7, column=1, padx=10, pady=10)
        self.add_wire_button.grid(row=7, column=2, padx=10, pady=10)
        self.lock_destination_checkbutton.grid(row=7, column=3, padx=10, pady=10)
        self.status_label.grid(
            row=8, column=0, columnspan=5, sticky="w", padx=10, pady=10
        )
        self.settings_button.grid(row=7, column=5, padx=10, pady=10)

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)

    def get_text_from_scrolledtext(self):
        return self.wire_list.get("1.0", "end-1c")

    def validate_csv_content(self, content):
        # Create a file-like object from the string for csv.reader
        csv_file_like_object = io.StringIO(content)

        reader = csv.reader(csv_file_like_object)
        for row in reader:
            if len(row) != 2:
                # Return the row number (plus 1 because csv.reader starts from 0)
                # where the validation failed
                return reader.line_num, row
        # If all rows are valid, return None
        return None

    def increment(self, input_box: tk.Entry):
        self.counter += 1
        current_value = input_box.get()
        try:
            current_value = int(current_value)
            new_value = current_value + 1
            input_box.delete(0, tk.END)
            input_box.insert(0, str(new_value))
        except ValueError:
            pass

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

        self.wire_manager.add_wire(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        self.wire_manager.save_to_csv()  # Autosave after adding a wire

        if self.cable_mode_toggle.get():
            # Format the wire labels for cable mode
            wire_label = (
                f"{source_component}-{source_terminal_block} [{source_terminal}]".upper()
                .replace("--", "-")
                .strip("-")
            )
            destination_label = (
                f"{destination_component}-{destination_terminal_block} [{destination_terminal}]".upper()
                .replace("--", "-")
                .strip("-")
            )
        else:
            wire_label = (
                f"{source_component}-{source_terminal_block}-{source_terminal}".upper()
                .replace("--", "-")
                .strip("-")
            )
            destination_label = (
                f"{destination_component}-{destination_terminal_block}-{destination_terminal}".upper()
                .replace("--", "-")
                .strip("-")
            )
        self.wire_list.insert(tk.END, f"{wire_label},{destination_label}\n")
        self.wire_list.see(tk.END)

        if self.source_increment_toggle.get():
            # Call increment method for the source and destination terminal
            self.increment(self.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.increment(self.destination_terminal_entry)

    def run_program(self):
        csv_file_name = self.csv_file_name.get()
        if is_valid_file_name(csv_file_name):
            self.wire_manager.set_csv_file_name(csv_file_name)
            self.wire_manager.load_from_csv(csv_file_name)

    def save_file(self) -> None:
        self.capitalize_scrolledtext()
        abs_file_path = self.csv_file_name.get()
        content = self.get_text_from_scrolledtext()

        # Update the content of scrolledtext widget to be uppercase
        self.wire_list.delete("1.0", tk.END)
        self.wire_list.insert("1.0", content)

        invalid_row = self.validate_csv_content(content)
        if invalid_row is not None:
            invalid_row_num, invalid_row_content = invalid_row
            tkinter.messagebox.showerror(
                title="Invalid CSV content",
                message=f"The CSV content you entered is invalid. "
                f"Each line should have exactly 2 columns, separated by a comma. "
                f"Please check line {invalid_row_num}: {invalid_row_content}",
            )
            return

        self.wire_manager.set_csv_file_name(abs_file_path)

        try:
            with open(abs_file_path, "w") as file:
                file.write(content)
            self.status_label.config(text=f"Successfully saved to {abs_file_path}")
            # After 5000 ms (5 seconds), reset the status_label text
            self.after(5000, lambda: self.status_label.config(text=""))
        except FileNotFoundError:
            tkinter.messagebox.showerror(
                title="File Not Found.",
                message=f"No file named {abs_file_path} was found.",
            )
            self.csv_file_name.set("")
            self.status_label.config(text="")

        self.label1.config(text=f"Saved CSV file name: {abs_file_path}")

    def load_wires(self):
        csv_file_name = self.csv_file_name.get()
        self.wire_manager.set_csv_file_name(csv_file_name)
        file_path = self.csv_file_name.get()

        # Check if file exists
        if not os.path.isfile(file_path):
            # Create an empty file if it doesn't exist
            open(file_path, "a").close()
        else:
            try:
                self.wire_manager.load_from_csv(file_path)
                with open(csv_file_name, "r") as file:
                    self.wire_list.insert(tk.END, file.read())
            except FileNotFoundError:
                tkinter.messagebox.showerror(
                    title="File Not Found",
                    message=f"No file named {csv_file_name} was found",
                )
                self.csv_file_name.set("")
