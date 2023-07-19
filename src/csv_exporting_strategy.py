import csv
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from src.connection import Connection

logger = logging.getLogger(__name__)


class ExportToCSVStrategy(ABC):
    @abstractmethod
    def export_to_csv(self, file_path: Path, connection_list: list[Connection]) -> None:
        pass


class ExportWireToCSVStrategy(ExportToCSVStrategy):
    def export_to_csv(self, file_path: Path, connection_list: list[Connection]) -> None:
        try:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                for connection in connection_list:
                    source = f"{connection.source_component}-{connection.source_terminal_block}-{connection.source_terminal}"
                    destination = f"{connection.destination_component}-{connection.destination_terminal_block}-{connection.destination_terminal}"
                    writer.writerow([source, destination])
            print("Successfully exported wires")
        except FileNotFoundError:
            logger.info(f"Error: Directory '{file_path}' not found")
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{file_path}'")
        except Exception as e:
            logger.info(f"Error: {e}")


class ExportCableToCSVStrategy(ExportToCSVStrategy):
    def export_to_csv(self, file_path: Path, connection_list: list[Connection]) -> None:
        try:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                for connection in connection_list:
                    source = f"{connection.source_component}-{connection.source_terminal_block} [{connection.source_terminal}]"
                    destination = f"{connection.destination_component}-{connection.destination_terminal_block} [{connection.destination_terminal}]"
                    writer.writerow([source, destination])
            print("Successfully exported cables")
        except FileNotFoundError:
            logger.info(f"Error: Directory '{file_path}' not found")
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{file_path}'")
        except Exception as e:
            logger.info(f"Error: {e}")
