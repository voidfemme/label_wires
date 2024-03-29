import csv
import logging
from typing import Any
from io import StringIO

from src.connection import Connection
from src.settings import Settings
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
    Manages the collection of Connection entities, ensuring data integrity, consistency,
    and providing CRUD operations on connections.
    """

    def __init__(self, full_file_path=None) -> None:
        """
        Initializes the ConnectionManager with an empty list of connections and other
        essential attributes.

        Args:
            full_file_path (str): The full file path to the saved connections JSON file.
        """
        self.settings = Settings()
        self.connections: list[Connection] = []
        self.observers = []
        self.full_file_path = full_file_path

    # Observer Methods to update the connection list in the GUI
    def add_observer(self, observer: Any) -> None:
        """
        Registers an observer to be notified of changes in connections.

        Args:
            observer: The observer entity to be added. (the 'self' of the class to be registered)
        """
        self.observers.append(observer)

    def remove_observer(self, observer: Any) -> None:
        """
        De-registers an observer, preventing it from receiving updates on connection changes.

        Args:
            observer: The observer entity to be removed
        """
        self.observers.remove(observer)

    def notify_observers(self, **kwargs) -> None:
        """
        Alerts all registered observers of changes to connections, ensuring synchronized updates.
        """
        for observer in self.observers:
            observer.update_connection_list(**kwargs)

    # Other methods
    def set_save_file_name(self, file_name: str) -> None:
        """
        Specifies the name of the file where connection data will be saved.

        Args:
            file_name (str): The desired name for the save file
        """
        self.full_file_path = file_name
        self.file_handler = FileHandler(self.full_file_path)

    def save_json_to_file(self) -> bool:
        """
        Converts connections to JSON and saves to file.

        Returns:
            bool: True if successful, False otherwise
        """
        data = [connection.to_dict() for connection in self.connections]
        success = self.file_handler.save(data)
        return success

    def populate_connections(self, conn_dicts) -> None:
        """
        Fills manager with connections from provided dictionaries.

        Args:
            conn_dicts (list): List of dictionaries representing connections.
        """
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
            return True
        else:
            return False

    def edit_connection(
        self, old_connection: Connection, new_connection: Connection
    ) -> bool:  # TODO: design tests for this method
        if old_connection in self.connections:
            # If new connection already exists or is the reverse of an existing connection,
            # don't do the edit
            if new_connection in self.connections:
                return False
            # Find the index of the old connection and replace it with the new one
            index = self.connections.index(old_connection)
            self.connections[index] = new_connection
            # Save updated connections to file
            self.save_json_to_file()
            return True
        else:
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
            self.notify_observers()
            return connection
        else:
            logger.info("Attempted to add duplicate or reverse duplicate connection.")
            raise DuplicateConnectionError("Duplicate connection attempted")

    def generate_csv_string(self) -> str:
        # Create a CSV string using StringIO
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)

        if self.connections:
            # Write headers
            headers = self.connections[0].to_dict().keys()
            csv_writer.writerow(headers)

            # Write connection data
            for connection in self.connections:
                csv_writer.writerow(connection.to_dict().values())

        # Reset the StringIO pointer to the beginning and get the CSV string
        csv_output.seek(0)
        csv_string = csv_output.getvalue()
        csv_output.close()

        return csv_string
