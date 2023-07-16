# Love is love. Be yourself
import logging

from tkinter import filedialog

from src.ui.main_view import MainView
from src.ui.new_project_dialog import NewProjectDialog

from src.file_handler import FileHandler
from src.settings import Settings
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem
from src.connection import Connection
from src.connection_manager import (
    ConnectionManager,
    NoFilePathGivenException,
    MalformedDataException,
)
from src.utility_functions import ExportFormat
from src.command import (
    AddConnectionCommand,
    EditConnectionCommand,
    DeleteConnectionCommand,
)
from src.csv_exporting_strategy import (
    ExportWireToCSVStrategy,
    ExportCableToCSVStrategy,
)

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        self.command_manager = CommandManager()
        self.event_system = EventSystem()  # Publish-Subscribe system for actions
        self.connection_manager = ConnectionManager()
        self.view = MainView(self, self.localizer)
        self.undo_stack = []
        self.full_file_path = None

    def initialize(self) -> None:
        """
        This function is called after the Controller instance has been created.
        It handles all of the additional setup that should not occur in the
        constructor (e.g. anything that involves calling methods on the Controller
        itself, or anything that might need to be mocked or stubbed in tests.)
        """
        self.wait_for_new_project_dialog()
        self.load_connections()

    def wait_for_new_project_dialog(self) -> None:
        self.new_project_dialog = NewProjectDialog(
            self.settings, self.localizer, self.view
        )
        self.view.wait_window(self.new_project_dialog)
        if self.new_project_dialog.result is not None:
            self.full_file_path = self.new_project_dialog.result.get("file_path", "")
        else:
            self.full_file_path = ""
        self.set_file_path(self.full_file_path)
        if self.full_file_path is not None and self.full_file_path != "":
            self.file_handler = FileHandler(self.full_file_path)
        else:
            return  # Figure out how I want to handle this case

    def get_file_path(self) -> None:
        self.file_name = filedialog.asksaveasfilename()

    def set_file_path(self, file_path: str) -> None:
        self.connection_manager.set_save_file_name(file_path)

    def populate_connections(self) -> None:
        self.load_from_json_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.view.tree_widget.insert("", "end", values=(source, destination))

    def load_connections(self) -> None:
        try:
            self.load_from_json_file()
        except NoFilePathGivenException as e:
            self.view.footer.display_status(str(e))
        self.view.tree_widget.update_connection_list()

    def edit_connection(self) -> None:
        # Get the currently selected connection.
        selected_items = self.view.tree_widget.selection()
        if not selected_items:
            return
        item = selected_items[0]  # Only one connection can be edited at once
        old_connection = self.view.tree_widget.tree_item_to_connection.get(item)
        if not old_connection:
            return

        # Put the old values into the entry boxes
        self.view.connection_entry_frame.populate_entries(old_connection)

        new_values = {
            "source_component": self.view.connection_entry_frame.source_component.get(),
            "source_terminal_block": self.view.connection_entry_frame.source_terminal_block.get(),
            "source_terminal": self.view.connection_entry_frame.source_terminal.get(),
            "destination_component": self.view.connection_entry_frame.destination_component.get(),
            "destination_terminal_block": self.view.connection_entry_frame.destination_terminal_block.get(),
            "destination_terminal": self.view.connection_entry_frame.destination_terminal.get(),
        }

        command = EditConnectionCommand(
            self.connection_manager, old_connection, new_values
        )
        self.command_manager.execute(command)

    def add_connection_command(
        self, source: dict[str, str], destination: dict[str, str]
    ) -> None:
        command = AddConnectionCommand(
            self.event_system, self.connection_manager, source, destination
        )
        self.command_manager.execute(command)

    def delete_connection_command(self) -> None:
        command = DeleteConnectionCommand(self, self.view)
        self.command_manager.execute(command)
        self.view.tree_widget.update_connection_list()

    def undo_connection_command(self) -> None:
        if self.command_manager.undo_stack:
            command = self.command_manager.undo_stack.pop()
            command.undo()

    def export_to_csv(self, format: ExportFormat) -> None:
        file_path = filedialog.asksaveasfilename(title="Save CSV as...")
        if file_path == "":
            return
        if format == ExportFormat.WIRE:
            strategy = ExportWireToCSVStrategy()
            print("Exported Wires successfully")
        elif format == ExportFormat.CABLE:
            strategy = ExportCableToCSVStrategy()
            print("Exported Cables successfully")
        else:
            raise ValueError(f"Invalid format: {format}")
        self.file_handler.export(
            file_path=file_path,
            strategy=strategy,
            data=self.connection_manager.connections,
        )

    def quit_program(self) -> None:
        self.view.destroy()

    def handle_quit(self) -> None:
        # Replacement for quit_program()
        if self.full_file_path:
            self.save_to_json_file()
        else:
            save = self.view.prompt_save()
            if save:
                file_path = self.view.open_save_dialog()
                if file_path:
                    self.full_file_path = file_path
                    self.save_to_json_file()

    def run(self) -> None:
        self.view.mainloop()

    def save_to_json_file(self) -> bool:
        data = [
            connection.to_dict() for connection in self.connection_manager.connections
        ]
        success = self.file_handler.save(data)
        return success

    def load_from_json_file(self) -> None:
        if self.full_file_path is not None:
            # Load in the connections from the file using the filehandler
            connection_dicts = self.file_handler.load()
            self.connection_manager.populate_connections(connection_dicts)
