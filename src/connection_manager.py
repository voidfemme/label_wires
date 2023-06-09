import csv
import string
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

from typing import List, Tuple, TypeVar, Generic, Type, Dict
from src.connection import Connection, Wire
from src.settings import Settings


logger = logging.getLogger(__name__)
ConnectionType = TypeVar("ConnectionType", bound=Connection)


class ConnectionManager(ABC, Generic[ConnectionType]):
    """
    This is the connection manager, which is responsible for managing the master list of wires.
    This class uses the observer pattern. To update the UI about its connection list. In the
    future, the UI should not handle this interaction directly, but instead the controller will
    handle the interaction for me.
    """

    def __init__(self, file_path) -> None:
        self.settings = Settings()
        self.file_path = file_path or self.settings.get("default_directory")
        self.connections: List[ConnectionType] = []
        self.observers = []

    def save_json_to_file(self) -> bool:
        try:
            with open(self.file_path, "w") as file:
                json.dump([conn.to_dict() for conn in self.connections], file, indent=4)
            return True
        except FileNotFoundError:
            logger.info(f"Error: File {self.file_path} not found.")
            return False
        except PermissionError:
            logger.info(f"Permission Error: could not write to: {self.file_path}")
            return False
        except ValueError:
            logger.info(f"ValueError: Could not write data to file.")
            return False
        except Exception as e:
            logger.info(f"Error: {e}")
            return False

    def load_json_from_file(self) -> None:
        try:
            with open(self.file_path, "r") as json_file:
                conn_dicts = json.load(json_file)
                self.validate_json_data(conn_dicts)

            self.connections = [  # type: ignore
                self.get_connection_class()(**conn_dict)
                for conn_dict in conn_dicts
                if not self.get_connection_class()(**conn_dict).is_empty()
            ]
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

    def is_valid_entry_string(self, input_string) -> bool:
        # Check that input is a string
        if not isinstance(input_string, str):
            return False

        # Check for control characters
        if any(char not in string.printable for char in input_string):
            return False

        # If it passes both checks, it's a valid string.
        return True

    def validate_json_data(self, input_data: List[Dict[str, str]]) -> None:
        required_fields = [
            "source_component",
            "source_terminal_block",
            "source_terminal",
            "destination_component",
            "destination_terminal_block",
            "destination_terminal",
        ]

        if not isinstance(input_data, list):
            raise ValueError("Invalid data: root element should be a list.")

        for item in input_data:
            if not isinstance(item, dict):
                raise ValueError(
                    "Invalid data: all elements in list should be dictionaries."
                )

            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Invalid data: missing '{field}'.")
                if not isinstance(item[field], str):
                    raise ValueError(f"Invalid data: '{field}' should be a string.")

    def delete_connection(self, connection_to_delete) -> bool:
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
            index = self.connections.index(old_connection)  # type: ignore
            self.connections[index] = new_connection  # type: ignore
            # Save updated connections to file
            self.save_json_to_file()
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
        # ^^ Explain why this is bad
        return self.connections[:]

    def export_to_csv(self, file_path) -> None:  # Perhaps consider returning a bool
        filename = Path(file_path)
        # Check if the file exists; I don't want to overwrite any existing csv files
        # Perhaps add a flag that will overwrite the file anyways when the user chooses.
        if filename.exists():
            raise FileExistsError(f"The file '{filename}' already exists.")
        # I could use a Strategy pattern to allow the user to choose the format of output
        # instead of having separate cable and wire objects
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f, delimiter="|")
                for connection in self.connections:
                    writer.writerow(connection.to_tuple())  # type: ignore
        except FileNotFoundError:
            logger.info(f"Error: Directory '{filename}' not found")
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{filename}'")
        except Exception as e:
            logger.info(f"Error: {e}")

    # Observer Methods to update the connection list in the GUI
    def add_observer(self, observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer.update_connection_list()

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
    ) -> bool:
        wire = Wire(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        logger.info(f"Adding wire: {wire}")
        # Use "not in" to access the Wire's __eq__ function to check for duplicates
        if wire not in self.connections:
            self.connections.append(wire)
            self.save_json_to_file()
            logger.info("Wire successfully added.")
            return True
        else:
            logger.info("Attempted to add duplicate or reverse wire.")
            return False
