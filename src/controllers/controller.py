# Love is love. Be yourself
import logging

from tkinter import filedialog
from src import connection_manager
from src.connection import Connection

from src.ui.main_view import MainView
from src.ui.new_project_dialog import NewProjectDialog

from src.file_handler import FileHandler
from src.settings import Settings
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem
from src.connection_manager import (
    ConnectionManager,
    NoFilePathGivenException,
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
    """
    The Controller class acts as an intermediary, managing the flow of data between the UI and the
    underlying logic. It interfaces with the UI components, CommandManager, and ConnectionManager to
    facilitate user actions such as adding, editing, and deleting connections.
    """

    def __init__(self) -> None:
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        self.command_manager = CommandManager()
        self.event_system = EventSystem()  # Publish-Subscribe system for actions
        self.connection_manager = ConnectionManager()
        self.view = MainView(controller=self, settings=self.settings)
        self.undo_stack = []
        self.full_file_path = None
        self.file_handler = FileHandler()

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
        """
        Awaits input or action from the New Project dialog window
        """
        self.view.withdraw()
        self.new_project_dialog = NewProjectDialog(
            self.settings, self.localizer, self.view
        )
        self.view.wait_window(self.new_project_dialog)

        # If we get a result from the new project dialog, set the file path, and open up the main
        # app, otherwise, set the file path to an empty string, so we can determine whether to quit
        # early
        if self.new_project_dialog.result is not None:
            self.full_file_path = self.new_project_dialog.result.get("file_path", "")
        else:
            self.full_file_path = ""
        self.set_file_path(self.full_file_path)

        # Show the main window if all the proper fields are set.
        if self.full_file_path is not None and self.full_file_path != "":
            self.file_handler = FileHandler(self.full_file_path)
            self.view.deiconify()
        else:
            return  # Figure out how I want to handle this case.

    def get_file_path(self) -> None:
        """
        Retrieves the path of the currently loaded file.

        Returns:
            str: The path of the loaded file.
        """
        self.file_name = filedialog.asksaveasfilename()

    def set_file_path(self, file_path: str) -> None:
        """
        Sets or updates the path of the loaded file.

        Args:
            path (str): The new file path to set.
        """
        self.connection_manager.set_save_file_name(file_path)

    def populate_connections(self) -> None:
        """
        Fills the UI's TreeWidgetFrame with connection data from the ConnectionManager.
        """
        self.load_from_json_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.view.tree_widget.insert("", "end", values=(source, destination))

    def load_connections(self) -> None:
        """
        Loads connections from a predefined source into the ConnectionManager
        """
        try:
            self.load_from_json_file()
        except NoFilePathGivenException as e:
            self.view.footer.display_status(str(e))
        self.view.tree_widget.update_connection_list()

    def update_connection_list(self):
        self.view.tree_widget.update_connection_list()

    def save_edited_connection_command(self) -> None:
        """
        saves a connection being edited based on user input or other triggers.
        """
        # Fetch the new values after user edits
        p1_values = {
            "source_component": self.view.entry_frame.source_component.get(),
            "source_terminal_block": self.view.entry_frame.source_terminal_block.get(),
            "source_terminal": self.view.entry_frame.source_terminal.get(),
        }
        p2_values = {
            "destination_component": self.view.entry_frame.destination_component.get(),
            "destination_terminal_block": self.view.entry_frame.destination_terminal_block.get(),
            "destination_terminal": self.view.entry_frame.destination_terminal.get(),
        }
        new_values = {
            "source_component": self.view.entry_frame.source_component.get(),
            "source_terminal_block": self.view.entry_frame.source_terminal_block.get(),
            "source_terminal": self.view.entry_frame.source_terminal.get(),
            "destination_component": self.view.entry_frame.destination_component.get(),
            "destination_terminal_block": self.view.entry_frame.destination_terminal_block.get(),
            "destination_terminal": self.view.entry_frame.destination_terminal.get(),
        }

        # Add the edited connection
        self.add_connection_command(p1_values, p2_values)

    def add_connection_command(
        self, source: dict[str, str], destination: dict[str, str]
    ) -> None:
        """
        Fetches and validates user input, then adds the connection.
        """
        command = AddConnectionCommand(
            self.event_system, self.connection_manager, source, destination
        )
        self.command_manager.execute(command)

    def delete_connection_command(self) -> None:
        """
        Identifies and safely removes the selected connection(s).
        """
        command = DeleteConnectionCommand(self, self.view)
        self.command_manager.execute(command)
        self.view.tree_widget.update_connection_list()

    def undo_connection_command(self) -> None:
        """
        Uses CommandManager to revert the latest change.
        """
        if self.command_manager.undo_stack:
            command = self.command_manager.undo_stack.pop()
            command.undo()

    def redo_connection_command(self) -> None:
        """
        Re-applies an action that was undone.
        """
        if self.command_manager.redo_stack:
            command = self.command_manager.redo_stack.pop()
            command.redo()

    def export_to_csv(self, format: ExportFormat) -> None:
        """
        Converts connections to CSV for easy sharing and analysis.

        Args:
            format (ExportFormat): The format of the resulting csv file
        """
        file_path = filedialog.asksaveasfilename(title="Save CSV as...")
        if file_path == "":
            return
        if format == ExportFormat.WIRE:
            strategy = ExportWireToCSVStrategy()
        elif format == ExportFormat.CABLE:
            strategy = ExportCableToCSVStrategy()
        else:
            raise ValueError(f"Invalid format: {format}")
        if self.file_handler is not None:
            self.file_handler.export(
                file_path=file_path,
                strategy=strategy,
                data=self.connection_manager.connections,
            )
        else:
            print("file handler not initialized")

    def quit_program(self) -> None:
        """
        Destroys the UI
        """
        self.view.destroy()

    def handle_quit(self, quit_from_dialog: bool) -> None:
        """
        Manages the quitting process, optionally saving data before exit.

        Args:
            quit_from_dialog (bool): Indicates if the quit action was triggered from a dialog.
        """
        if quit_from_dialog:
            # Return early because we're not saving a file
            self.quit_program()
            return

        # Save the file before quitting
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
        """
        Initiates the main program loop.
        """
        self.view.mainloop()

    def save_to_json_file(self) -> bool:
        """
        Saves connection data as a JSON file.

        Returns:
            bool: Success status of the save operation.
        """
        data = [
            connection.to_dict() for connection in self.connection_manager.connections
        ]
        success = self.file_handler.save(data)
        return success

    def load_from_json_file(self) -> None:
        """
        Loads connections from a JSON file if a file path exists.
        """
        if self.full_file_path is not None:
            # Load in the connections from the file using the filehandler
            connection_dicts = self.file_handler.load()
            self.connection_manager.populate_connections(connection_dicts)

    def display_status(self, message):
        """
        Displays a status message in the UI's footer.

        Args:
            message: The status message to display
        """
        self.view.footer.display_status(message)
