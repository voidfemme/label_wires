import tkinter as tk
import logging
from tkinter import ttk, messagebox, filedialog

from src.utility_functions import TEMPORARY_FILE_LOCATION
from src.ui.settings_window import SettingsWindow
from src.ui.header import Header
from src.ui.tree_widget_frame import TreeWidgetFrame
from src.ui.connection_entry_frame import ConnectionEntryFrame
from src.ui.utility_buttons import UtilityButtonsFrame
from src.ui.footer import Footer


logger = logging.getLogger(__name__)


class MainView(tk.Tk):
    def __init__(
        self,
        controller,
        localizer,
        settings,
        connection_manager,
        command_manager,
        event_system,
    ) -> None:
        super().__init__()
        self.controller = controller
        self.localizer = localizer
        self.title(self.localizer.get("application_title"))
        self.settings = settings
        self.command_manager = command_manager
        self.event_system = event_system
        self.connection_manager = connection_manager

        self.geometry("1200x400")
        self.create_widgets()
        self.arrange_widgets_in_grid()
        self.tree_widget.update_connection_list()

    def create_widgets(self) -> None:
        print("Creating Widgets")
        # Define labels
        self.header = Header(
            self, self.localizer, self.settings, TEMPORARY_FILE_LOCATION
        )

        # Define text area for connection numbers
        self.tree_widget = TreeWidgetFrame(
            self,
            self.localizer,
            self.settings,
            self.connection_manager,
            self.command_manager,
            self.event_system,
        )
        self.connection_entry_frame = ConnectionEntryFrame(
            self,
            self.controller,
            self.localizer,
            self.settings,
            self.connection_manager,
            self.command_manager,
            self.event_system,
        )

        self.utility_buttons_horizontal_rule = ttk.Separator(self, orient="horizontal")

        self.utility_buttons_frame = UtilityButtonsFrame(
            self, self.localizer, self.connection_manager
        )

        self.horizontal_rule_footer = ttk.Separator(self, orient="horizontal")
        self.footer = Footer(self, self.localizer, self.settings)

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

    def display_error_messagebox(self, title, message=""):
        try:
            messagebox.showerror(self.localizer.get(title), self.localizer.get(message))
        except Exception as e:
            # Add error handling for KeyError
            logger.warn(e)

    def saved_to_json_file(self) -> None:
        return self.connection_manager.save_json_to_file()

    def save_file(self):
        if self.connection_manager.saved_to_json_file():
            self.display_status(
                self.localizer.get("success_file_added").format(TEMPORARY_FILE_LOCATION)
            )
        else:
            self.display_status(self.localizer.get("error_file_added"))

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
        self.destroy()
