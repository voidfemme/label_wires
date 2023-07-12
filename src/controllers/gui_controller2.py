#!/usr/bin/env python3
import sys
import logging

from src.connection_manager import WireManager
from src.settings import Settings
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem
from src.command import DeleteConnectionCommand

from src.ui.connection_app import ConnectionApp
from src.ui.new_project_dialog import NewProjectDialog

logger = logging.getLogger(__name__)


class Controller:
    """
    New Controller class to handle all the interactions of the UI. I'm going to try and make the
    Controller monolithic, so that I can coordinate all the elements of the UI together.

    This means that I'll need to create methods for interacting with the connection_manager
    and event_system.  The Controller is a two-way relationship with the UI, so once I give
    the UI a backbone and a set of functions, then I can work

    Create each element of the UI here and give the frames
    """

    def __init__(self, model: WireManager, view=None) -> None:
        self.model = model
        self.view = ConnectionApp()

        self.command_manager = CommandManager()
        self.event_system = EventSystem()  # Make sure to utilize this
        self.undo_stack = []

        self.file_name = self.wait_for_new_project_dialog()

    def wait_for_new_project_dialog(self) -> str:
        self.new_project_dialog = NewProjectDialog(self.view)
        self.view.wait_window(self.view)
        self.new_project_result = self.new_project_dialog.result

        if self.new_project_result is None:
            self.view.display_error_messagebox(
                "Error", "Could not get new project data. Quitting."
            )
            self.view.destroy()
            sys.exit(1)
        else:
            return self.new_project_result.get("file_name")  # hmmmmmm

    def export_to_csv(self) -> None:
        filename = self.view.display_file_browser(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if filename:
            try:
                self.model.export_to_csv(filename)
                self.view.display_status(self.view.localizer.get("exported_file"))
            except FileExistsError as e:
                self.view.display_status(message=str(e))

    def saved_to_json_file(self) -> None:
        self.model.save_json_to_file

    def loaded_from_json_file(self) -> None:
        self.model.load_json_from_file()

    def update_connection_list(self) -> None:
        for i in self.view.tree_widget.get_children():
            self.view.tree_widget.delete(i)

        connections = self.view.connection_manager.get_connections()

        for connection in connections:
            source, destination = self.view.connection_manager.get_connection_tuple(
                connection
            )
            item_id = self.view.tree_widget.insert(
                "", "end", values=(source, destination)
            )

            self.view.tree_widget.connections_dict[str(connection)] = connection
            self.view.tree_widget.tree_item_to_connection[item_id] = connection

    def update_selected_connections(self, event) -> None:
        print(event)
        # Get currently selected items
        selected_items = self.view.tree_widget.selection()

        # Clear the selected connections list
        self.view.tree_widget.selected_connections = []

        # Add all currently selected connections to the list
        for item in selected_items:
            connection = self.view.tree_widget.tree_item_to_connection.get(item)
            if connection:
                self.view.tree_widget.selected_connections.append(connection)

        logger.info(
            f"self.view.selected_connections = {self.view.tree_widget.selected_connections}"
        )

    def populate_tree_widget(self) -> None:
        self.loaded_from_json_file()
        for connection in self.model.get_connections():
            source, destination = self.model.get_connection_tuple(connection)
            self.view.tree_widget.insert("", "end", values=(source, destination))

    def add_connection(self) -> None:
        # Get user input from the UI
        source = {
            "component": self.view.connection_entry_frame.source_component.get(),
            "terminal_block": self.view.connection_entry_frame.source_terminal_block.get(),
            "terminal": self.view.connection_entry_frame.source_terminal.get(),
        }

        # Set destination fields to match source fields
        destination = {
            "component": self.view.connection_entry_frame.destination_component.get(),
            "terminal_block": self.view.connection_entry_frame.destination_terminal_block.get(),
            "terminal": self.view.connection_entry_frame.destination_terminal.get(),
        }

    def run(self) -> None:
        pass


model = WireManager("file/path")
controller = Controller(model)
