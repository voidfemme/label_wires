import tkinter as tk

from src.localized_widgets import LocalizedButton


class UtilityButtonsFrame(tk.Frame):
    def __init__(self, parent, localizer, connection_manager, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.localizer = localizer
        self.connection_manager = connection_manager
        self.create_and_place_buttons()

    # Wrapper Functions
    def call_parent_method(self, method_name, *args, **kwargs):
        method = getattr(self.parent, method_name, None)
        if method:
            return method(*args, **kwargs)
        else:
            raise AttributeError(f"No such method: {method_name}")

    def get_parent_attribute(self, attribute_name):
        attribute = getattr(self.parent, attribute_name, None)
        if attribute is None:
            raise AttributeError(f"No such attribute: {attribute_name}")
        return attribute

    def create_and_place_buttons(self):
        self.save_button = LocalizedButton(
            self,
            self.localizer,
            "save_file",
            command=self.parent.save_file
        )
        self.save_button.grid(row=0, column=0, padx=5, pady=10)

        self.settings_button = LocalizedButton(
            self,
            self.localizer,
            "settings",
            command=self.parent.open_settings_window
        )
        self.settings_button.grid(row=0, column=1, padx=5, pady=10)

        self.export_button = LocalizedButton(
            self,
            self.localizer,
            "export",
            command=self.parent.export_to_csv
        )
        self.export_button.grid(row=0, column=2, padx=5, pady=10)

        self.quit_button = LocalizedButton(
            self,
            self.localizer,
            "quit",
            command=self.parent.quit_program
        )
        self.quit_button.grid(row=0, column=3, padx=5, pady=10)
