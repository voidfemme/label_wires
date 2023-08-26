import logging
from pathlib import Path

from src.connection import Connection
from src.settings import Settings
from src.utility_functions import validate_json_wire_fields
from src.csv_exporting_strategy import ExportToCSVStrategy
from src.file_handler import FileHandler


logger = logging.getLogger(__name__)


class NoFilePathGivenException(Exception):
    pass


class MalformedDataException(Exception):
    pass


class DuplicateConnectionError(Exception):
    pass


class ConnectionManager:
    """
    This is the connection manager, which is responsible for managing the master list of wires.
    This class uses the observer pattern. To update the UI about its connection list. In the
    future, the UI should not handle this interaction directly, but instead the controller will
    handle the interaction for me.
    """

    def __init__(self, full_file_path=None) -> None:
        self.settings = Settings()
        self.connections: list[Connection] = []
        self.observers = []
        self.full_file_path = full_file_path

    # Observer Methods to update the connection list in the GUI
    def add_observer(self, observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update_connection_list()

    # Other methods
    def set_save_file_name(self, file_name: str) -> None:
        self.full_file_path = file_name
        self.file_handler = FileHandler(self.full_file_path)

    def save_json_to_file(self) -> bool:
        """
        This method should not be here, but I'm unsure of how exactly to remove it
        without breaking the treewidget.
        """
        data = [connection.to_dict() for connection in self.connections]
        success = self.file_handler.save(data)
        return success

    def populate_connections(self, conn_dicts) -> None:
        if conn_dicts is not None:
            self.connections = [
                Connection(**conn_dict)
                for conn_dict in conn_dicts
                if not Connection(**conn_dict).is_empty()
            ]  # **conn_dict is because we're unpacking the dictionary into the Wire object

    def delete_connection(self, connection_to_delete: Connection) -> bool:
        if connection_to_delete in self.connections:
            self.connections.remove(connection_to_delete)
            self.save_json_to_file()
            logger.info("connection successfully deleted.")
            return True
        else:
            logger.info("Attempted to delete a connection that doesn't exist.")
            return False

    def edit_connection(
        self, old_connection: Connection, new_connection: Connection
    ) -> bool:  # TODO: design tests for this method
        if old_connection in self.connections:
            # If new connection already exists or is the reverse of an existing connection,
            # don't do the edit
            if new_connection in self.connections:
                logger.info(
                    "Attempted to edit connection into a duplicate or reverse duplicate connection."
                )
                return False
            # Find the index of the old connection and replace it with the new one
            index = self.connections.index(old_connection)
            self.connections[index] = new_connection
            # Save updated connections to file
            self.save_json_to_file()
            return True
        else:
            logger.info("Attempted to edit a connection that doesn't exist.")
            return False

    def get_connection_tuple(self, connection: Connection) -> tuple[str, str]:
        if connection not in self.connections:
            return ("", "")
        return connection.to_tuple()

    def get_connections(self) -> list[Connection]:
        # Return a copy of the list of connections. Return a *copy* because returning the
        # object itself can alow external code to mutate the internal state of the class.
        return self.connections[:]

    def add_connection(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ) -> Connection:
        connection = Connection(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        logger.info(f"Adding connection: {connection}")
        # Use "not in" to access the Wire's __eq__ function to check for duplicates
        if connection not in self.connections:
            self.connections.append(connection)
            self.save_json_to_file()
            logger.info("Connection successfully added.")
            return connection
        else:
            logger.info("Attempted to add duplicate or reverse duplicate connection.")
            raise DuplicateConnectionError("Duplicate connection attempted")
