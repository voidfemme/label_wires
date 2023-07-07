import csv
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, TypeVar, Generic, Type
from src.connection import Connection, Cable, Wire
from src.settings import Settings
from src.validation import is_valid_file_path, is_valid_entry_string, validate_json_data

"""
This is the connection manager, which is responsible for managing the master list of wires.
"""

logger = logging.getLogger(__name__)
ConnectionType = TypeVar("ConnectionType", bound=Connection)


class ConnectionManager(ABC, Generic[ConnectionType]):
    def __init__(self, file_path) -> None:
        self.settings = Settings()
        self.file_path = file_path or self.settings.get("default_directory")
        if not is_valid_file_path(file_path):
            raise ValueError(f"Invalid file path: {file_path}")
        self.connections: List[ConnectionType] = []

    def save_to_file(self) -> bool:
        try:
            with open(self.file_path, "w") as file:
                json.dump([conn.to_dict() for conn in self.connections], file, indent=4)
            return True
        except FileNotFoundError:
            logger.info(f"Error: File {self.file_path} not found.")
            return False

    def load_from_file(self) -> None:
        try:
            with open(self.file_path, "r") as json_file:
                conn_dicts = json.load(json_file)
                validate_json_data(conn_dicts)

            self.connections = [
                self.get_connection_class()(**conn_dict)
                for conn_dict in conn_dicts
                if not self.get_connection_class()(**conn_dict).is_empty()
            ]
            for conn in self.connections:
                logger.info(f"Loaded connection: {conn}")
            logger.info(f"JSON file loaded as {self.file_path}")
        except FileNotFoundError:
            logger.info(f"Error: Directory '{self.file_path}' not found")
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{self.file_path}'")
        except ValueError:
            logger.info(
                f"Error: Invalid JSON data. Please inspect the input file: {self.file_path}"
            )
        except Exception as e:
            logger.info(f"Error loading JSON file: {e}")

    def delete_connection(self, connection_to_delete) -> bool:
        if connection_to_delete in self.connections:
            self.connections.remove(connection_to_delete)
            self.save_to_file()
            logger.info("connection successfully deleted.")
            return True
        else:
            logger.info("Attempted to delete a connection that doesn't exist.")
            return False

    def edit_connection(
        self, old_connection: Connection, new_connection: Connection
    ) -> bool:
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
            self.save_to_file()
            return True
        else:
            logger.info("Attempted to edit a connection that doesn't exist.")
            return False

    def get_connection_tuple(self, connection) -> Tuple[str, str]:
        if connection not in self.connections:
            return ("", "")
        return connection.to_tuple()

    def get_connections(self) -> List[ConnectionType]:
        # Return a copy of the list of connections. Return a copy because returning the
        # object itself can alow external code to mutate the internal state of the class.
        return self.connections[:]

    def export_to_csv(self, file):
        filename = Path(file)
        # Check if the file exists
        if filename.exists():
            raise FileExistsError(f"The file '{filename}' already exists.")

        # Run a check to make sure there aren't commas in the data fields. I know my default
        # delimiter is already a pipe symbol, but I want it to be a comma by default, but
        # adapt to the user's needs. After writing the file to csv, I could maybe raise an error
        # of some kind, catch that by the connection_app and print a message to tell the user
        # what kind of delimiter to use.
        
        # TODO: Cables and wires have different formats, and I want to support more advanced
        # cable operations in the future.

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f, delimiter="|")
            for connection in self.connections:
                writer.writerow(connection.to_tuple())

    @abstractmethod
    def add_connection(self, *args) -> bool:
        pass

    @abstractmethod
    def get_connection_class(self) -> Type[Connection]:
        """This method should return the class of the connection manager"""
        pass


class WireManager(ConnectionManager[Wire]):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.connections: List[Wire] = []

    def get_connection_class(self) -> Type[Wire]:
        return Wire

    def add_connection(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ):
        wire = Wire(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        inputs = [
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        ]

        if not all(is_valid_entry_string(input) for input in inputs):
            logger.info("invalid input")
            return False

        logger.info(f"Adding wire: {wire}")
        if wire not in self.connections:
            self.connections.append(wire)
            self.save_to_file()
            logger.info("Wire successfully added.")
            return True
        else:
            logger.info("Attempted to add duplicate or reverse wire.")
            return False


class CableManager(ConnectionManager[Cable]):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.connections: List[Cable] = []

    def get_connection_class(self) -> Type[Cable]:
        return Cable

    def add_connection(
        self,
        source_component: str,
        source_terminal_block: str,
        source_terminal: str,
        destination_component: str,
        destination_terminal_block: str,
        destination_terminal: str,
    ) -> bool:
        cable = Cable(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        inputs = [
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        ]

        if not all(is_valid_entry_string(input) for input in inputs):
            logger.info("invalid input")
            return False

        logger.info(f"Adding cable: {cable}")
        if cable not in self.connections:
            self.connections.append(cable)
            self.save_to_file()
            logger.info("Cable successfully added.")
            return True
        else:
            logger.info("Attempted to add duplicate cable.")
            return False
