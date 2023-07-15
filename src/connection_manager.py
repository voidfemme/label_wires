import json
import logging
from pathlib import Path

from typing import List, Tuple
from src.connection import Connection
from src.settings import Settings
from src.utility_functions import validate_json_wire_fields
from src.csv_exporting_strategy import ExportToCSVStrategy


logger = logging.getLogger(__name__)


class NoFilePathGivenException(Exception):
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
        self.connections: List[Connection] = []
        self.observers = []
        self.full_file_path = full_file_path

    def set_save_file_name(self, file_name: str) -> None:
        self.full_file_path = file_name

    def save_json_to_file(self) -> bool:
        if not self.full_file_path:
            raise NoFilePathGivenException("No file path provided. Cannot Save")
        try:
            with open(self.full_file_path, "w") as file:
                json.dump([conn.to_dict() for conn in self.connections], file, indent=4)
            return True
        except FileNotFoundError:
            logger.info(f"Error: File {self.full_file_path} not found.")
            return False
        except PermissionError:
            logger.info(f"Permission Error: could not write to: {self.full_file_path}")
            return False
        except ValueError:
            logger.info("ValueError: Could not write data to file.")
            return False
        except Exception as e:
            logger.info(f"Error: {e}")
            return False

    def load_json_from_file(self) -> None:
        if not self.full_file_path:
            raise NoFilePathGivenException("No file path provided. Cannot Load")
        try:
            with open(self.full_file_path, "r") as json_file:
                conn_dicts = json.load(json_file)
                validate_json_wire_fields(conn_dicts)

            self.connections = [
                Connection(**conn_dict)
                for conn_dict in conn_dicts
                if not Connection(**conn_dict).is_empty()
            ]  # **conn_dict is because we're unpacking the dictionary into the Wire object
            logger.info(f"JSON file loaded as {self.full_file_path}")
        except FileNotFoundError:
            logger.info(f"Error, {self.full_file_path} not found. Creating a new file")
            with open(self.full_file_path, "w"):
                pass
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{self.full_file_path}'")
        except ValueError:
            logger.info(
                f"Error: Invalid JSON data. Please inspect the input file: {self.full_file_path}"
            )
        except Exception as e:
            logger.info(f"Error loading JSON file: {e}")

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

    def get_connection_tuple(self, connection: Connection) -> Tuple[str, str]:
        if connection not in self.connections:
            return ("", "")
        return connection.to_tuple()

    def get_connections(self) -> List[Connection]:
        # Return a copy of the list of connections. Return a copy because returning the
        # object itself can alow external code to mutate the internal state of the class.
        return self.connections[:]

    def export_to_csv(self, file_path: str, strategy: ExportToCSVStrategy) -> None:
        full_file_path = Path(file_path)
        if full_file_path.exists():
            raise FileExistsError(
                f"The file '{full_file_path}' already exists. Cannot overwrite."
            )
        strategy.export_to_csv(full_file_path, self.connections)

    # Observer Methods to update the connection list in the GUI
    def add_observer(self, observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update_connection_list()

    def add_connection(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ) -> bool:
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
            return True
        else:
            logger.info("Attempted to add duplicate or reverse duplicate connection.")
            return False
