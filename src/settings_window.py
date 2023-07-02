import tkinter as tk
from tkinter import filedialog, ttk
from src.localizer import Localizer


class SettingsWindow(tk.Toplevel):
    def __init__(self, master, settings, language="en", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.settings = settings
        self.localizer = Localizer(language)

        self.title(self.localizer.get("settings"))

        # Add setting controls here:
        self.create_language_section()
        self.create_default_save_section()
        self.create_csv_save_location_section()

        self.save_button = tk.Button(
            self, text=self.localizer.get("save_settings"), command=self.save_settings
        )
        self.save_button.pack(side=tk.TOP, padx=5, pady=5)

    def create_language_section(self):
        self.languages = ["en", "ru", "fr", "es", "shakespeare"]
        self.language_label = tk.Label(self, text=self.localizer.get("language"))
        self.language_combobox = ttk.Combobox(self, values=self.languages)
        self.language_combobox.current(
            self.languages.index(self.settings.get("language", "en"))
        )

        self.language_label.pack(side=tk.TOP, padx=5, pady=5)
        self.language_combobox.pack(side=tk.TOP, padx=5, pady=5)

    def create_default_save_section(self):
        self.default_save_location_label = tk.Label(
            self, text=self.localizer.get("default_save_location")
        )
        self.default_save_location_entry = tk.Entry(self)
        self.default_save_location_entry.insert(
            0, self.settings.get("default_save_location", "")
        )
        self.default_save_location_browse_button = tk.Button(
            self,
            text=self.localizer.get("browse"),
            command=lambda: self.browse_directory(self.default_save_location_entry),
        )

        self.default_save_location_label.pack(side=tk.TOP, padx=5, pady=5)
        self.default_save_location_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.default_save_location_browse_button.pack(side=tk.TOP, padx=5, pady=5)

    def create_csv_save_location_section(self):
        self.csv_save_location_label = tk.Label(
            self, text=self.localizer.get("csv_save_location")
        )
        self.csv_save_location_entry = tk.Entry(self)
        self.csv_save_location_entry.insert(
            0, self.settings.get("csv_save_location", "")
        )
        self.csv_save_location_browse_button = tk.Button(
            self,
            text=self.localizer.get("browse"),
            command=lambda: self.browse_directory(self.csv_save_location_entry),
        )

        self.csv_save_location_label.pack(side=tk.TOP, padx=5, pady=5)
        self.csv_save_location_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.csv_save_location_browse_button.pack(side=tk.TOP, padx=5, pady=5)

    def browse_directory(self, entry_field):
        directory = filedialog.askdirectory()
        if directory:  # User didn't cancel the dialog
            entry_field.delete(0, tk.END)
            entry_field.insert(0, directory)

    def save_settings(self):
        self.settings.set("language", self.language_combobox.get())
        self.settings.set(
            "default_save_location", self.default_save_location_entry.get()
        )
        self.settings.set("csv_save_location", self.csv_save_location_entry.get())
        self.settings.save_settings()
