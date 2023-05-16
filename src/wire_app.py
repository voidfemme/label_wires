#!/usr/bin/env python3
# Workers of the world, Unite!
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext
from src.wire_manager import GUIWireManager, WIRENUMS_DIR, is_valid_file_name


class WireApp(tk.Tk):
    def __init__(self, file_name: str):
        super().__init__()

        self.title("Wire Manager")

        # csv file name
        self.data_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "label_wires", "data"
        )
        abs_file_path = os.path.join(self.data_dir, file_name + ".csv")
        self.csv_file_name = tk.StringVar(value=abs_file_path)

        self.wire_manager = GUIWireManager(self.csv_file_name.get(), WIRENUMS_DIR)
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

    def create_widgets(self):
        # Define labels
        self.label1 = tk.Label(self, textvariable=self.csv_file_name)
        self.component_label = tk.Label(self, text="Component")
        self.terminal_block_label = tk.Label(self, text="Terminal Block")
        self.terminal_label = tk.Label(self, text="Terminal")
        self.file_name_field_label = tk.Label(self, text="Saving as:")

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

        # Define text area for wire numbers
        self.wire_list = scrolledtext.ScrolledText(self, width=30, height=15)

        # Define buttons
        self.save_button = tk.Button(self, text="Save File", command=self.save_file)
        self.add_wire_button = tk.Button(self, text="Add Wire", command=self.add_wire)
        self.save_button = tk.Button(
            self,
            text="Save File",
            command=self.wire_manager.save_to_csv,
        )

        # Define bindings
        self.destination_terminal_entry.bind("<Return>", lambda event: self.add_wire())
        self.file_name_field.bind("<Return>", lambda event: self.save_file())

        # Define Checkbuttons
        self.source_increment_checkbutton = tk.Checkbutton(
            self, text="Increment", variable=self.source_increment_toggle
        )
        self.destination_increment_checkbutton = tk.Checkbutton(
            self, text="Increment", variable=self.destination_increment_toggle
        )

        # Arrange widgets in grid (left to right, top to bottom)
        self.wire_list.grid(row=1, column=0, rowspan=6, padx=10, pady=10)
        self.file_name_field_label.grid(row=1, column=1, padx=10, pady=10)
        self.file_name_field.grid(row=1, column=2, columnspan=3, sticky="ew", padx=10, pady=10)

        self.component_label.grid(row=3, column=2, padx=10, pady=10)
        self.terminal_block_label.grid(row=3, column=3, padx=10, pady=10)
        self.terminal_label.grid(row=3, column=4, padx=10, pady=10)

        self.source_increment_checkbutton.grid(row=5, column=1, padx=10, pady=10)
        self.source_component_entry.grid(row=5, column=2, padx=10, pady=10)
        self.source_terminal_block_entry.grid(row=5, column=3, padx=10, pady=10)
        self.source_terminal_entry.grid(row=5, column=4, padx=10, pady=10)

        self.destination_increment_checkbutton.grid(row=6, column=1, padx=10, pady=10)
        self.destination_component_entry.grid(row=6, column=2, padx=10, pady=10)
        self.destination_terminal_block_entry.grid(row=6, column=3, padx=10, pady=10)
        self.destination_terminal_entry.grid(row=6, column=4, padx=10, pady=10)

        self.add_wire_button.grid(row=7, column=2, padx=10, pady=10)
        self.save_button.grid(row=7, column=4, padx=10, pady=10)

    def increment(self, input_box: tk.Entry):
        self.counter += 1

        current_value = int(input_box.get())
        new_value = current_value + 1
        input_box.delete(0, tk.END)
        input_box.insert(0, str(new_value))

    def add_wire(self):
        source_component = self.source_component.get()
        source_terminal_block = self.source_terminal_block.get()
        source_terminal = self.source_terminal.get()

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

        self.wire_list.insert(
            tk.END,
            f"{source_component}-{source_terminal_block}-{source_terminal} "
            f", {destination_component}-{destination_terminal_block}-{destination_terminal}\n".upper(),
        )
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
        csv_file_name = self.csv_file_name.get()
        self.wire_manager.set_csv_file_name(csv_file_name)
        try:
            self.wire_manager.load_from_csv(csv_file_name)
            with open(csv_file_name, "r") as file:
                self.wire_list.insert(tk.END, file.read())
        except FileNotFoundError:
            tkinter.messagebox.showerror(
                title="File Not Found.",
                message=f"No file named {csv_file_name} was found.",
            )
            self.csv_file_name.set("")

        self.label1.config(text=f"Saved CSV file name: {csv_file_name}")

    def load_wires(self):
        csv_file_name = self.csv_file_name.get()
        self.wire_manager.set_csv_file_name(csv_file_name)
        file_path = os.path.join(WIRENUMS_DIR, f"{self.csv_file_name}.csv")
        try:
            self.wire_manager.load_from_csv(file_path)
            with open(f"{self.csv_file_name.get()}.csv", "r") as file:
                self.wire_list.insert(tk.END, file.read())
        except FileNotFoundError:
            tkinter.messagebox.showerror(
                title="File Not Found",
                message=f"No file named {self.csv_file_name.get()}.csv was found",
            )
            self.csv_file_name.set("")  # Clear the StringVar for the file name


