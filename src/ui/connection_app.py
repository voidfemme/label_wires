# Love is love. Be yourself
import logging
import sys

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from src.settings import Settings
from src.settings_window import SettingsWindow
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem
from src.connection_manager import WireManager

from src.ui.header import Header
from src.ui.tree_widget_frame import TreeWidgetFrame
from src.ui.connection_entry_frame import ConnectionEntryFrame
from src.ui.utility_buttons import UtilityButtonsFrame
from src.ui.footer import Footer
from src.ui.new_project_dialog import NewProjectDialog

from src.controllers.gui_controller import GUIController

logger = logging.getLogger(__name__)

"""
Perhaps I should put the Controller logic back into this, and instead extract the GUI
code and turn this into the controller
"""


class ConnectionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        # Localizer belongs here bc it's an integral part of the UI

        self.title(self.localizer.get("application_title"))
        self.command_manager = CommandManager()
        self.event_system = EventSystem()  # Publish-Subscribe system for actions
        self.gui_controller = GUIController(self)
        self.undo_stack = []

        # TODO: Allow Windows OS to automatically set the window size
        # TODO: Set default font for both Windows and Linux
        # Set the default window size
        self.geometry("1200x400")

        # Hide the main window
        self.withdraw()

        # Show new project dialog and wait for result
        self.wait_for_new_project_dialog()

        # Initialize ConnectionManager
        self.gui_controller.initialize_connection_manager()

        self.create_widgets()
        self.load_connections()
        self.deiconify()

    def wait_for_new_project_dialog(self):
        print("Waiting for new project dialog")
        # Call NewProjectDialog and wait until it's done
        self.new_project_dialog = NewProjectDialog(self)
        self.wait_window(self.new_project_dialog)
        self.new_project_result = self.new_project_dialog.result

        if self.new_project_result is None:
            self.quit()
            return

        # Get results from NewProjectDialog
        self.file_name = self.new_project_result.get("file_name")
        self.file_path = self.new_project_result.get("file_path")

    def create_widgets(self) -> None:
        print("Creating Widgets")
        # Define labels
        self.header = Header(self, self.localizer, self.settings, self.file_name)

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

        self.arrange_widgets_in_grid()
        self.tree_widget.update_connection_list()

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

    def open_settings_window(self) -> None:
        self.settings_window = SettingsWindow(self, self.settings)

    def edit_connection(self) -> None:
        pass

    def populate_connections(self) -> None:
        self.connection_manager.load_json_from_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.tree_widget.insert("", "end", values=(source, destination))

    def run_program(self) -> None:
        try:
            if self.file_path is None:
                self.file_path = "untitled"
            self.connection_manager = WireManager(self.file_path)
        except ValueError as e:
            # Allow the user to manually select a mode
            logger.info(f"Error: {e}")
            sys.exit(1)  # or however you want to handle this case

    def save_file(self) -> None:
        if self.gui_controller.saved_to_json_file():
            self.display_status(
                self.localizer.get("success_file_added").format(self.file_path)
            )
        else:
            self.display_status(self.localizer.get("error_file_added"))

    def load_connections(self):
        self.gui_controller.loaded_from_json_file()
        self.tree_widget.update_connection_list()

    def export_to_csv(self) -> None:
        self.gui_controller.export_to_csv()

    def display_status(self, message) -> None:
        # Update the status label with the message
        self.footer.display_status(message)

    def display_file_browser(self, *args, **kwargs):
        return filedialog.asksaveasfilename(*args, **kwargs)

    def display_error_messagebox(self, title, message=""):
        try:
            messagebox.showerror(self.localizer.get(title), self.localizer.get(message))
        except Exception as e:
            # Add error handling for KeyError
            logger.warn(e)

    def quit_program(self) -> None:
        self.destroy()
        sys.exit(0)
