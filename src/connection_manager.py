import csv
import json
import logging
import re
import string
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, TypeVar, Generic, Type
from src.connection import Connection, Cable, Wire
from src.settings import Settings

logger = logging.getLogger(__name__)
ConnectionType = TypeVar("ConnectionType", bound=Connection)


def is_valid_file_path(path: str) -> bool:
    file_path = Path(path)
    dir_name = file_path.parent
    file_name = file_path.name

    if os.name == "nt":  # For Windows systems
        valid_path_chars = not bool(re.search(r'[<>:"|?*]|\.$|\s$', file_name))
    else:  # For Unix/Linux based systems
        valid_path_chars = "\0" not in path

    # Check if path exists and if it has write Permissions
    path_exists = dir_name.exists()
    can_write = os.access(dir_name, os.W_OK)

    if not path_exists:
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not can_write:
        raise PermissionError(f"No write permissions for path: {path}")

    return valid_path_chars


def is_valid_entry_string(input_string) -> bool:
    # Check that input is a string
    if not isinstance(input_string, str):
        return False

    # Check for control characters
    if any(char not in string.printable for char in input_string):
        return False

    # If it passes both checks, it's a valid string.
    return True


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
            # If new connection already exists or is the reverse of an existing connection, don't do the edit
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
