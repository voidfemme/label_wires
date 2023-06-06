import tkinter as tk
from tkinter import scrolledtext, ttk
from src.wire_app import WireApp

# Fix circular import with WireApp by removing WireApp calls from this class

class DestinationWiringFrame(ttk.Frame):
    def __init__(
        self, master, wireapp, csv_file_name=None, wire_list=None, wire_manager=None, **kwargs
    ) -> None:
        super().__init__(master, **kwargs)
        self.label = tk.Label(self, text="Source and Destination of wire has different labels")
        self.label.pack()
        self.csv_file_name = csv_file_name  # stringvar
        self.wire_list = wire_list  # ScrolledText widget
        self.wire_manager = wire_manager  # GUIWireManager instance

    def create_widgets(self):
        # Use wireapp's elements
        self.csv_file_name_field = self.wireapp.csv_file_name_field
        self.save_button = self.wireapp.save_button
        self.wire_list = self.wireapp.wire_list

        # Define variables
        self.csv_file_name = tk.StringVar()
        self.source_component = tk.StringVar()
        self.source_terminal_block = tk.StringVar()
        self.source_terminal = tk.StringVar()
        self.destination_component = tk.StringVar()
        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal = tk.StringVar()
        self.source_increment_toggle = tk.BooleanVar()
        self.destination_increment_toggle = tk.BooleanVar()

        # Define labels
        self.label1 = tk.Label(self, textvariable=self.csv_file_name)
        self.component_label = tk.Label(self, text="Component")
        self.terminal_block_label = tk.Label(self, text="Terminal Block")
        self.terminal_label = tk.Label(self, text="Terminal")
        self.file_name_field_label = tk.Label(self, text="Saving as:")
        self.source_label = tk.Label(self, text="Source ->")
        self.destination_label = tk.Label(self, text="Destination ->")

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
        self.save_button = tk.Button(
            self, text="Save File", command=self.wire_manager.save_file
        )
        self.add_wire_button = tk.Button(
            self, text="Add Wire", command=self.wire_manager.add_wire
        )

        # Define bindings
        self.source_component_entry.bind(
            "<Return>", lambda event: self.wire_manager.add_wire()
        )
        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.wire_manager.add_wire()
        )
        self.source_terminal_entry.bind(
            "<Return>", lambda event: self.wire_manager.add_wire()
        )
        self.destination_component_entry.bind(
            "<Return>", lambda event: self.wire_manager.add_wire()
        )
        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.wire_manager.add_wire()
        )
        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.wire_manager.add_wire()
        )
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

        self.add_wire_button.grid(row=7, column=2, padx=10, pady=10)
