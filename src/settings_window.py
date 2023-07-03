import tkinter as tk
from tkinter import filedialog, ttk
from src.localizer import Localizer
from src.localized_widgets import (
    LocalizedLabel,
    LocalizedButton,
    LocalizedCombobox,
    LocalizedTreeView,
    LocalizedCheckButton,
)


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
        # self.create_caps_lock_section()

        self.save_button = LocalizedButton(
            self, self.localizer, "save", command=self.save_settings
        )
        self.cancel_button = LocalizedButton(
            self, self.localizer, "cancel", command=self.destroy
        )
        self.save_button.pack(side=tk.TOP, padx=5, pady=5)

    def create_language_section(self):
        self.languages = ["en", "ru", "fr", "es", "shakespeare"]
        self.create_language_separator = ttk.Separator(self, orient="horizontal")
        self.language_label = LocalizedLabel(self, self.localizer, "language")
        self.language_combobox = ttk.Combobox(self, values=self.languages)
        self.language_combobox.current(
            self.languages.index(self.settings.get("language", "en"))
        )

        self.language_label.pack(side=tk.TOP, padx=5, pady=5)
        self.language_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.create_language_separator.pack(side=tk.TOP, pady=5)

    def create_default_save_section(self):
        self.create_default_save_separator = ttk.Separator(self, orient="horizontal")
        self.default_save_location_label = LocalizedLabel(
            self, self.localizer, "default_save_location"
        )
        self.default_save_location_entry = tk.Entry(self)
        self.default_save_location_entry.insert(
            0, self.settings.get("default_save_location", "")
        )
        self.default_save_location_browse_button = LocalizedButton(
            self,
            self.localizer,
            "browse",
            command=lambda: self.browse_directory(self.default_save_location_entry),
        )

        self.default_save_location_label.pack(side=tk.TOP, padx=5, pady=5)
        self.default_save_location_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.default_save_location_browse_button.pack(side=tk.TOP, padx=5, pady=5)
        self.create_default_save_separator.pack(side=tk.TOP, pady=5)

    def create_csv_save_location_section(self):
        self.create_csv_save_separator = ttk.Separator(self, orient="horizontal")
        self.csv_delimiter_separator = ttk.Separator(self, orient="horizontal")
        self.csv_save_location_label = LocalizedLabel(
            self, self.localizer, "csv_save_location"
        )
        self.csv_delimiter_label = LocalizedLabel(self, self.localizer, "default_csv_delimiter")
        self.csv_save_location_entry = tk.Entry(self)
        self.csv_save_location_entry.insert(
            0, self.settings.get("csv_save_location", "")
        )
        self.csv_save_location_browse_button = LocalizedButton(
            self,
            self.localizer,
            "browse",
            command=lambda: self.browse_directory(self.csv_save_location_entry),
        )
        self.csv_delimiter_entry = tk.Entry(self)
        self.csv_delimiter_entry.insert(
            0, self.settings.get("default_csv_delimiter", "")
        )

        self.csv_save_location_label.pack(side=tk.TOP, padx=5, pady=5)
        self.csv_save_location_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.csv_save_location_browse_button.pack(side=tk.TOP, padx=5, pady=5)
        self.create_csv_save_separator.pack(side=tk.TOP, pady=5)
        self.csv_delimiter_label.pack(side=tk.TOP, padx=5, pady=5)
        self.csv_delimiter_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.csv_delimiter_separator.pack(side=tk.TOP, pady=5)

    def browse_directory(self, entry_field):
        directory = filedialog.askdirectory()
        if directory:  # User didn't cancel the dialog
            entry_field.delete(0, tk.END)
            entry_field.insert(0, directory)

    def save_settings(self):
        new_locale = self.language_combobox.get()
        self.settings.set("language", new_locale)
        self.settings.set(
            "default_save_location", self.default_save_location_entry.get()
        )
        self.settings.set("csv_save_location", self.csv_save_location_entry.get())
        print(f"New locale: {new_locale}")
        print(f"Language in settings file: {self.settings.get('language')}")
        LocalizedLabel.update_all()
        LocalizedButton.update_all()
        LocalizedCheckButton.update_all()
        LocalizedTreeView.update_all()
        LocalizedCombobox.update_all()
        self.settings.save_settings()
        self.update_idletasks()
        self.destroy()
