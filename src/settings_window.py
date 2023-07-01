import tkinter as tk
from src.settings import settings


class SettingsWindow(tk.Toplevel):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.title("Settings")

        # Setting the default file save location
        self.default_save_location = tk.StringVar()

        # Toggle upper case conversion
        self.upper_case_conversion = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        # Define labels
        self.save_location_label = tk.Label(self, text="Default File Save Location")
        self.upper_case_conversion_label = tk.Label(self, text="All Caps Mode")

        # Define Entry fields
        self.save_location_field = tk.Entry(
            self, textvariable=self.default_save_location
        )

        # Define Buttons
        self.save_button = tk.Button(
            self, text="Save Settings", command=self.save_settings
        )

        # Define Checkbuttons
        self.upper_case_conversion_checkbutton = tk.Checkbutton(
            self, text="Enable", variable=self.upper_case_conversion
        )

        # Arrange widgets in grid
        self.save_location_label.grid(row=0, column=0, padx=10, pady=10)
        self.save_location_field.grid(row=0, column=1, padx=10, pady=10)
        self.upper_case_conversion_label.grid(row=1, column=0, padx=10, pady=10)
        self.upper_case_conversion_checkbutton.grid(row=1, column=1, padx=10, pady=10)
        self.save_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def save_settings(self):
        # Here you can define what happens when the user saves the settings
        # For example, you might want to save the default file save location somewhere
        pass

    def change_default_directory(self):
        new_path = "/new/path/to/default/directory"
        settings.set_default_directory(new_path)
