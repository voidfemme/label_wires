# Love is love. Be yourself
import logging

from tkinter import filedialog

from src.ui.main_view import MainView

from src.settings import Settings
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem
from src.connection_manager import ConnectionManager, NoFilePathGivenException
from src.utility_functions import (
    ExportFormat,
)
from src.command import AddConnectionCommand
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
        self.connection_manager = ConnectionManager(self)
        self.view = MainView(
            self,
            self.localizer,
            self.settings,
        )
        self.undo_stack = []
        self.file_name = ""

        self.load_connections()

    def get_file_path(self):
        self.file_name = filedialog.asksaveasfilename()

    def set_file_path(self, file_path):
        self.connection_manager.full_file_path = file_path

    def edit_connection(self) -> None:
        pass

    def populate_connections(self) -> None:
        self.connection_manager.load_json_from_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.view.tree_widget.insert("", "end", values=(source, destination))

    def load_connections(self) -> None:
        if self.view.header.get_file_path() == "":
            self.view.footer.display_status(
                "Could not load from file, no file location specified."
            )
        try:
            self.load_from_json_file()
        except NoFilePathGivenException as e:
            self.view.footer.display_status(str(e))
        self.view.tree_widget.update_connection_list()

    def add_connection_command(self, source: str, destination: str) -> None:
        cmd = AddConnectionCommand(
            self.event_system, self.connection_manager, source, destination
        )
        self.command_manager.execute(cmd)

    def undo_connection_command(self) -> None:
        if self.command_manager.undo_stack:
            command = self.command_manager.undo_stack.pop()
            command.undo()

    def export_to_csv(self, format: ExportFormat) -> None:
        file_path = filedialog.asksaveasfilename(title="Save CSV as...")
        if format == ExportFormat.WIRE:
            strategy = ExportWireToCSVStrategy()
            print("Exported Wires successfully")
        elif format == ExportFormat.CABLE:
            strategy = ExportCableToCSVStrategy()
            print("Exported Cables successfully")
        else:
            raise ValueError(f"Invalid format: {format}")
        self.connection_manager.export_to_csv(file_path=file_path, strategy=strategy)

    def quit_program(self) -> None:
        self.view.destroy()

    def run(self):
        self.view.mainloop()

    def save_to_json_file(self) -> bool:
        try:
            return self.connection_manager.save_json_to_file()
        except NoFilePathGivenException as e:
            self.view.display_status(str(e))
            return False

    def load_from_json_file(self) -> None:
        self.connection_manager.load_json_from_file()
