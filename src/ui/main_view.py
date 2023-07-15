import tkinter as tk
import logging
from tkinter import ttk, messagebox, filedialog

from src.ui.settings_window import SettingsWindow
from src.ui.header import Header
from src.ui.tree_widget_frame import TreeWidgetFrame
from src.ui.connection_entry_frame import ConnectionEntryFrame
from src.ui.utility_buttons import UtilityButtonsFrame
from src.ui.footer import Footer


logger = logging.getLogger(__name__)

"""
Main View in the MVC (Model-View-Controller) pattern. This module instantiates and
manages the various frames that make up its contents.
"""


class MainView(tk.Tk):
    def __init__(
        self,
        controller,
        localizer,
        settings,
    ) -> None:
        super().__init__()
        self.controller = controller
        self.title(self.controller.localizer.get("application_title"))
        self.settings = settings
        self.geometry("1200x400")
        self.create_widgets()
        self.arrange_widgets_in_grid()
        self.tree_widget.update_connection_list()

    def create_widgets(self) -> None:
        print("Creating Widgets")
        # Define labels
        self.header = Header(
            self,
            self.controller,
        )

        # Define text area for connection numbers
        self.tree_widget = TreeWidgetFrame(
            self,
            self.controller,
            self.controller.event_system,
        )
        self.connection_entry_frame = ConnectionEntryFrame(
            self,
            self.controller,
        )

        self.utility_buttons_horizontal_rule = ttk.Separator(self, orient="horizontal")

        self.utility_buttons_frame = UtilityButtonsFrame(
            self, self.controller, self.controller.localizer
        )

        self.horizontal_rule_footer = ttk.Separator(self, orient="horizontal")
        self.footer = Footer(
            self, self.controller, self.controller.localizer, self.settings
        )

    def arrange_widgets_in_grid(self) -> None:
        print("Arranging widgets")
        # Arrange widgets in grid (left to right, top to bottom)
        self.header.grid(row=0, column=0, sticky="ew")
        self.tree_widget.grid(row=1, column=0, rowspan=6, padx=5, pady=5)
        self.connection_entry_frame.grid(row=1, column=1, padx=5, pady=5)
        self.utility_buttons_horizontal_rule.grid(
            row=3, column=1, columnspan=5, sticky="ew", pady=5
        )
        self.utility_buttons_frame.grid(row=4, column=1, padx=5, pady=5)
        self.horizontal_rule_footer.grid(
            row=5, column=1, columnspan=5, sticky="ew", pady=5
        )
        self.footer.grid(row=6, column=1, sticky="ew")

    def scroll_to_bottom_of_treewidget(self) -> None:
        self.tree_widget.tree_widget.update_idletasks()
        self.tree_widget.tree_widget.yview_moveto(1)

    def save_file(self):
        file_name = self.controller.file_name
        if self.controller.save_to_json_file():
            self.display_status(
                self.controller.localizer.get("success_file_added").format(file_name)
            )
        else:
            self.display_status(self.controller.localizer.get("error_file_added"))

    def display_status(self, message) -> None:
        # Update the status label with the message
        self.footer.display_status(message)

    def open_settings_window(self) -> None:
        self.settings_window = SettingsWindow(self, self.settings)

    def export_to_csv(self) -> None:
        self.controller.export_to_csv()

    def display_file_browser(self, *args, **kwargs):
        return filedialog.asksaveasfilename(*args, **kwargs)

    def quit_program(self) -> None:
        # Check to see if a file name has been supplied. If it has, save and quit. Otherwise, prompt
        # the user with a save-dialog box. Allow the user to export to csv and trash the contents
        # as well.

        # Handle the "Don't save" case
        if self.controller.full_file_path:
            self.controller.save_to_json_file()
            self.destroy()
        else:
            # Ask the user if they want to save
            save = messagebox.askyesno(
                title=self.controller.localizer.get("unsaved_changes"),
                message=self.controller.localizer.get("save_changes_prompt"),
            )
            if save:
                # If the user wants to save, show a save dialog
                file_path = filedialog.asksaveasfilename(
                    title=self.controller.localizer.get("save_file"),
                    filetypes=[
                        ("JSON files", "*.json"),
                        ("Wire files", "*.wir"),
                        ("All files", "*.*"),
                    ],
                    defaultextension=".wir",
                )
                if file_path:
                    # If the user selected a file, save the work
                    self.controller.full_file_path = file_path
                    self.controller.save_to_json_file()
        self.destroy()
