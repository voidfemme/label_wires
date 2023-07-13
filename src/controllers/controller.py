# Love is love. Be yourself
import logging

from tkinter import filedialog

from src.ui.main_view import MainView
from src.settings import Settings
from src.localizer import Localizer
from src.command_manager import CommandManager
from src.event_system import EventSystem
from src.connection_manager import WireManager
from src.utility_functions import TEMPORARY_FILE_LOCATION

logger = logging.getLogger(__name__)

"""
Perhaps I should put the Controller logic back into this, and instead extract the GUI
code and turn this into the controller
"""


class Controller:
    def __init__(self) -> None:
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        self.connection_manager = WireManager(TEMPORARY_FILE_LOCATION)
        self.command_manager = CommandManager()
        self.event_system = EventSystem()  # Publish-Subscribe system for actions
        self.view = MainView(
            self,
            self.localizer,
            self.settings,
            self.connection_manager,
            self.command_manager,
            self.event_system,
        )
        self.undo_stack = []

        self.load_connections()

    def edit_connection(self) -> None:
        pass

    def populate_connections(self) -> None:
        self.connection_manager.load_json_from_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.view.tree_widget.insert("", "end", values=(source, destination))

    def load_connections(self):
        self.loaded_from_json_file()
        self.view.tree_widget.update_connection_list()

    def export_to_csv(self) -> None:
        self.export_to_csv()

    def display_file_browser(self, *args, **kwargs):
        return filedialog.asksaveasfilename(*args, **kwargs)

    def quit_program(self) -> None:
        self.view.destroy()

    def run(self):
        self.view.mainloop()

    def saved_to_json_file(self) -> None:
        self.connection_manager.save_json_to_file()

    def loaded_from_json_file(self) -> None:
        self.connection_manager.load_json_from_file()
