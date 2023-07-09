# Love is love. Be yourself
import json
import logging
import sys

import tkinter as tk
from tkinter import messagebox, filedialog

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

from src.ui.header import Header
from src.ui.tree_widget_wire_list import TreeWidgetFrame
from src.ui.connection_entry_frame import ConnectionEntryFrame
from src.ui.utility_buttons import UtilityButtonsFrame

logger = logging.getLogger(__name__)


class ConnectionApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        self.title(self.localizer.get("application_title"))
        self.command_manager = CommandManager()
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

        # Sources
        self.source_increment_toggle = tk.BooleanVar()
        self.source_component = tk.StringVar()
        self.source_terminal_block = tk.StringVar()
        self.source_terminal = tk.StringVar()

        # Destinations
        self.destination_increment_toggle = tk.BooleanVar()
        self.destination_component = tk.StringVar()
        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal = tk.StringVar()

        # Lock destination input to match what the user types in source input
        # Perhaps do this live in the near future
        self.lock_destination_toggle = tk.BooleanVar()

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
        )
        self.connection_entry_frame = ConnectionEntryFrame(
            self,
            self.localizer,
            self.settings,
            self.connection_manager,
            self.command_manager,
        )

        self.status_label = tk.Label(self, text="")
        self.utility_buttons_frame = UtilityButtonsFrame(
            self, self.localizer, self.connection_manager
        )

        self.arrange_widgets_in_grid()
        self.update_connection_list()

    def arrange_widgets_in_grid(self) -> None:
        print("Arranging widgets")
        # Arrange widgets in grid (left to right, top to bottom)
        self.header.grid(row=0, column=0, stick="ew")
        self.tree_widget.grid(row=1, column=0, rowspan=6, padx=5, pady=5)
        self.connection_entry_frame.grid(row=1, column=1, padx=5, pady=5)
        self.utility_buttons_frame.grid(row=2, column=1, padx=5, pady=5)

    def update_selected_connections(self, event) -> None:
        logger.info(f"event = {event}")

        # Get currently selected items
        selected_items = self.tree_widget.selection()
        logger.info(f"selected_items: {selected_items}")

        # Clear the selected connections list
        self.selected_connections = []

        # Add all currently selected connections to the list
        for item in selected_items:
            connection = self.tree_item_to_connection.get(item)
            if connection:
                self.selected_connections.append(connection)
                logger.info(f"selected_connections: {self.selected_connections}")

        logger.info(f"self.selected_connections = {self.selected_connections}")

    def open_settings_window(self) -> None:
        self.settings = Settings()
        self.settings_window = SettingsWindow(self, self.settings)

    def increment(self, input_box: tk.Entry) -> None:
        try:
            value = int(input_box.get())
            input_box.delete(0, tk.END)
            input_box.insert(0, str(value + 1))
        except ValueError:
            self.display_status(self.localizer.get("increment_error"))

    def is_empty_label(
        self,
        source_component,
        source_terminal_block,
        source_terminal,
        destination_component,
        destination_terminal_block,
        destination_terminal,
    ) -> bool:
        return (
            source_component == ""
            and source_terminal_block == ""
            and source_terminal == ""
            and destination_component == ""
            and destination_terminal_block == ""
            and destination_terminal == ""
        )

    def add_connection(self) -> None:
        source = {
            "component": self.source_component.get(),
            "terminal_block": self.source_terminal_block.get(),
            "terminal": self.source_terminal.get(),
        }

        if self.lock_destination_toggle.get():
            # Set destination fields to match source fields
            self.destination_component.set(source["component"])
            self.destination_terminal_block.set(source["terminal_block"])
            self.destination_terminal.set(source["terminal"])

        destination = {
            "component": self.destination_component.get(),
            "terminal_block": self.destination_terminal_block.get(),
            "terminal": self.destination_terminal.get(),
        }

        # Check if every field is empty
        if self.is_empty_label(
            source["component"],
            source["terminal_block"],
            source["terminal"],
            destination["component"],
            destination["terminal_block"],
            destination["terminal"],
        ):
            return

        cmd = AddConnectionCommand(self, source, destination)
        self.command_manager.execute(cmd)

        if self.source_increment_toggle.get():
            self.increment(self.connection_entry_frame.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.increment(self.connection_entry_frame.destination_terminal_entry)
        self.tree_widget.yview_moveto(1)
        print(f"added connection")

    def handle_delete_button_clicked(self) -> None:
        command = DeleteConnectionCommand(self)
        self.command_manager.execute(command)
        self.update_connection_list()

    def edit_connection(self) -> None:
        # First, make sure only one item was selected.

        # Then, populate the fields with the item's values.

        # Use an EditConnectionCommand in order to be able to re-add the old connection
        # command = EditConnectionCommand(self)
        pass

    def undo(self) -> None:
        if self.command_manager.undo_stack:
            command = self.command_manager.undo_stack.pop()
            command.undo()

    def populate_connections(self) -> None:
        self.connection_manager.load_json_from_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.tree_widget.insert("", "end", values=(source, destination))

    def update_connection_list(self) -> None:
        self.tree_widget.delete(
            *self.tree_widget.get_children()
        )  # clear the tree widget

        for connection in self.connection_manager.connections:
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            # Add to the tree widget and get unique identifier
            item_id = self.tree_widget.insert("", "end", values=(source, destination))

            # Add to the dictionaries
            self.connections_dict[str(connection)] = connection
            self.tree_item_to_connection[item_id] = connection

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
            logger.info(f"Error: {e}")
            sys.exit(1)  # or however you want to handle this case

    def save_file(self) -> None:
        success = self.connection_manager.save_json_to_file()

        if success:
            self.display_status(
                self.localizer.get("success_file_added").format(self.file_path)
            )
        else:
            self.display_status(self.localizer.get("error_file_added"))

    def load_connections(self):
        self.connection_manager.load_json_from_file()
        self.update_connection_list()

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
        self.status_label["text"] = message

        # Clear the status label after 5 seconds
        self.after(5000, lambda: self.status_label.config(text=""))

    def quit_program(self) -> None:
        self.destroy()
        sys.exit(0)
