import tkinter as tk
from tkinter import filedialog


class Header(tk.Frame):
    def __init__(self, parent, controller, localizer, settings):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.localizer = localizer
        self.settings = settings
        self.create_and_place_elements()

    def create_and_place_elements(self):
        self.file_name_label = tk.Label(self, text="File Name: ")
        self.file_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.file_name_entry = tk.Entry(self)
        self.file_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.file_name_browse_button = tk.Button(
            self, text="Browse", command=self.browse
        )
        self.file_name_browse_button.grid(row=0, column=2, padx=5, pady=5)
        self.set_file_path_button = tk.Button(
            self, text="Set File Path", command=self.get_file_path
        )
        self.set_file_path_button.grid(row=0, column=3, padx=5, pady=5)

    def browse(self):
        filename = filedialog.asksaveasfilename()
        # Clear the entry box
        self.file_name_entry.delete(0, tk.END)
        # Insert the selected file path into the entry box
        self.file_name_entry.insert(0, filename)
        self.controller.get_file_path()

    def get_file_path(self):
        file_path = self.file_name_entry.get()
        # Check if the file path is just a base name
        if "/" not in file_path and "\\" not in file_path:
            # Prepend the default save location
            file_path = self.settings.get("default_save_location") + "/" + file_path
            if not file_path.endswith(".csv"):
                file_path = file_path + ".csv"
        self.controller.set_file_path(file_path)
