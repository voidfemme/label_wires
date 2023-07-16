import tkinter as tk
from typing import TYPE_CHECKING

from src.ui.localized_widgets import LocalizedButton
from src.utility_functions import ExportFormat

if TYPE_CHECKING:
    from src.controllers.controller import Controller
    from src.localizer import Localizer


class UtilityButtonsFrame(tk.Frame):
    def __init__(
        self, parent, controller: "Controller", localizer: "Localizer", **kwargs
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.localizer = localizer
        self.create_and_place_buttons()

    def get_parent_attribute(self, attribute_name: str) -> None:
        attribute = getattr(self.parent, attribute_name, None)
        if attribute is None:
            raise AttributeError(f"No such attribute: {attribute_name}")
        return attribute

    def create_and_place_buttons(self) -> None:
        self.save_button = LocalizedButton(
            self, self.localizer, "save_file", command=self.on_save_button_click
        )
        self.save_button.grid(row=0, column=0, padx=5, pady=10)

        self.settings_button = LocalizedButton(
            self, self.localizer, "settings", command=self.parent.open_settings_window
        )
        self.settings_button.grid(row=0, column=1, padx=5, pady=10)

        self.export_wires_button = LocalizedButton(
            self,
            self.localizer,
            "export_wires",
            command=self.on_export_wires_button_click,
        )
        self.export_wires_button.grid(row=0, column=2, padx=5, pady=10)

        self.export_cables_button = LocalizedButton(
            self,
            self.localizer,
            "export_cables",
            command=self.on_export_cables_button_click,
        )
        self.export_cables_button.grid(row=0, column=3, padx=5, pady=10)

        self.quit_button = LocalizedButton(
            self, self.localizer, "quit", command=self.on_quit_button_click
        )
        self.quit_button.grid(row=0, column=4, padx=5, pady=10)

    def on_quit_button_click(self) -> None:
        self.controller.quit_program()

    def on_export_wires_button_click(self) -> None:
        self.controller.export_to_csv(ExportFormat.WIRE)

    def on_export_cables_button_click(self) -> None:
        self.controller.export_to_csv(ExportFormat.CABLE)

    def on_save_button_click(self) -> None:
        self.controller.save_to_json_file()
