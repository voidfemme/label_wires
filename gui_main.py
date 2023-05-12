#!/usr/bin/env python3
# Workers of the world, Unite!
import tkinter as tk
from tkinter import filedialog, scrolledtext
from label_wires.wire_manager import GUIWireManager, WIRENUMS_DIR, is_valid_file_name


class WireApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Wire Manager")

        self.csv_file_name = tk.StringVar()
        self.filter_by = tk.StringVar()
        self.filter_value = tk.StringVar()
        self.wire_manager = GUIWireManager(self.csv_file_name.get(), WIRENUMS_DIR)

        self.source_component = tk.StringVar()
        self.source_terminal_block = tk.StringVar()
        self.source_terminal = tk.StringVar()

        self.destination_component = tk.StringVar()
        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal = tk.StringVar()

        self.label1 = tk.Label(self)
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Saving the File
        self.label1 = tk.Label(self, textvariable=self.csv_file_name)
        self.label1.grid(row=1, column=1, padx=10, pady=10)

        self.entry1 = tk.Entry(self, textvariable=self.csv_file_name)
        self.entry1.grid(row=1, column=1, padx=10, pady=10)
        self.entry1.bind("<Return>", lambda event: self.save_file())

        # self.browse_button = tk.Button(self, text="Browse", command=self.browse)
        # self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Save File", command=self.save_file)
        self.save_button.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        self.source_component = tk.StringVar()
        self.source_component_entry = tk.Entry(self, textvariable=self.source_component)
        self.source_component_entry.grid(row=5, column=2, padx=10, pady=10)

        self.source_terminal_block = tk.StringVar()
        self.source_terminal_block_entry = tk.Entry(
            self, textvariable=self.source_terminal_block
        )
        self.source_terminal_block_entry.grid(row=5, column=3, padx=10, pady=10)

        self.source_terminal = tk.StringVar()
        self.source_terminal_entry = tk.Entry(self, textvariable=self.source_terminal)
        self.source_terminal_entry.grid(row=5, column=4, padx=10, pady=10)

        self.destination_component = tk.StringVar()
        self.destination_component_entry = tk.Entry(
            self, textvariable=self.destination_component
        )
        self.destination_component_entry.grid(row=6, column=2, padx=10, pady=10)

        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal_block_entry = tk.Entry(
            self, textvariable=self.destination_terminal_block
        )
        self.destination_terminal_block_entry.grid(row=6, column=3, padx=10, pady=10)

        self.destination_terminal = tk.StringVar()
        self.destination_terminal_entry = tk.Entry(
            self, textvariable=self.destination_terminal
        )
        self.destination_terminal_entry.grid(row=6, column=4, padx=10, pady=10)
        self.destination_terminal_entry.bind("<Return>", lambda event: self.add_wire())

        self.add_wire_button = tk.Button(self, text="Add Wire", command=self.add_wire)
        self.add_wire_button.grid(row=7, column=2, padx=10, pady=10)

        self.wire_list = scrolledtext.ScrolledText(self, width=30, height=15)
        self.wire_list.grid(row=1, column=0, rowspan=6, padx=10, pady=10)

        self.save_button = tk.Button(
            self,
            text=f"Save File as {self.csv_file_name}",
            command=self.wire_manager.save_to_csv,
        )
        self.save_button.grid(row=7, column=4, padx=10, pady=10)

    def browse(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_file_name.set(file_path)

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
            f", {destination_component}-{destination_terminal_block}-{destination_terminal}\n",
        )

    def run_program(self):
        csv_file_name = self.csv_file_name.get()

        if is_valid_file_name(csv_file_name):
            wire_manager = GUIWireManager(csv_file_name, WIRENUMS_DIR)
            wire_manager.load_from_csv()

    def save_file(self) -> None:
        csv_file_name = self.csv_file_name.get()
        self.wire_manager = GUIWireManager(csv_file_name, WIRENUMS_DIR)
        self.wire_manager.save_to_csv()

        # update the label with the saved file name
        self.label1.config(text=f"Saved CSV file name: {csv_file_name}")


if __name__ == "__main__":
    app = WireApp()
    app.mainloop()
