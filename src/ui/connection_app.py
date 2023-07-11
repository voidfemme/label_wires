# Love is love. Be yourself
import logging
import sys

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from src.command import (
    AddConnectionCommand,
    DeleteConnectionCommand,
    EditConnectionCommand,
)
from src.settings import Settings
from src.settings_window import SettingsWindow
from src.new_project_dialog import NewProjectDialog
from src.connection_manager_factory import ConnectionManagerFactory
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem

from src.ui.header import Header
from src.ui.tree_widget_frame import TreeWidgetFrame
from src.ui.connection_entry_frame import ConnectionEntryFrame
from src.ui.utility_buttons import UtilityButtonsFrame
from src.ui.footer import Footer

logger = logging.getLogger(__name__)


class ConnectionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        self.title(self.localizer.get("application_title"))
        self.command_manager = CommandManager()
        self.event_system = EventSystem()  # Publish-Subscribe system for actions
        self.undo_stack = []

        # Set the default window size
        self.geometry("1200x400")

        # Hide the main window
        self.withdraw()

        # Show new project dialog and wait for result
        self.wait_for_new_project_dialog()

        self.initialize_connection_lists()

        # Initialize ConnectionManager
        self.initialize_connection_manager()

        self.create_widgets()
        self.load_connections()
        self.deiconify()

    def initialize_connection_lists(self):
        # Initialize lists for managing wires
        self.connections_dict = {}  # holds the list of connections in the treewidget

        # quick lookup table to map from tree widget item identifiers to the connections in your
        # application.
        self.tree_item_to_connection = {}

        self.selected_connections = []  # user-selected connections

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
        self.entry_mode = self.new_project_result.get("mode")
        self.file_path = self.new_project_result.get("file_path")

    def initialize_connection_manager(self):
        # Initialize the ConnectionManager
        print("Initializing Connection Manager")
        if self.entry_mode and self.file_path:
            self.connection_manager = (
                ConnectionManagerFactory.create_connection_manager(
                    self.entry_mode, self.file_path
                )
            )
        else:
            messagebox.showerror(
                self.localizer.get("error"),
                self.localizer.get("error_connection_manager_init"),
            )
            sys.exit(0)

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
            self.event_system
        )
        self.connection_entry_frame = ConnectionEntryFrame(
            self,
            self.localizer,
            self.settings,
            self.connection_manager,
            self.command_manager,
            self.event_system
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
            if self.entry_mode is None:
                self.entry_mode = "connection"
            self.connection_manager = (
                ConnectionManagerFactory.create_connection_manager(
                    self.entry_mode, self.file_path
                )
            )
        except ValueError as e:
            # Allow the user to manually select a mode
            logger.info(f"Error: {e}")
            sys.exit(1)  # or however you want to handle this case

    def save_file(self) -> None:
        # Ask the connection manager to save the file
        success = self.connection_manager.save_json_to_file()

        if success:
            self.display_status(
                self.localizer.get("success_file_added").format(self.file_path)
            )
        else:
            self.display_status(self.localizer.get("error_file_added"))

    def load_connections(self):
        self.connection_manager.load_json_from_file()
        self.tree_widget.update_connection_list()

    def export_to_csv(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if filename:  # if a filename was entered in the dialog
            try:
                self.connection_manager.export_to_csv(filename)
                self.display_status(self.localizer.get("exported_file"))
            except FileExistsError as e:
                self.display_status(str(e))

    def display_status(self, message) -> None:
        # Update the status label with the message
        self.footer.display_status(message)

    def quit_program(self) -> None:
        self.destroy()
        sys.exit(0)
