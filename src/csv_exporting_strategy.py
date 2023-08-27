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
            if not file_path.suffix == ".csv":
                file_path = file_path.with_suffix("")
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                for conn in connection_list:
                    source = f"{conn.source_component}-{conn.source_terminal_block}-{conn.source_terminal}".strip(
                        "-"
                    )
                    destination = f"{conn.destination_component}-{conn.destination_terminal_block}-{conn.destination_terminal}".strip(
                        "-"
                    )
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
            if not file_path.suffix == ".csv":
                file_path = file_path.with_suffix(".csv")
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file, delimiter="|")
                for conn in connection_list:
                    source = (
                        f"{conn.source_component}-{conn.source_terminal_block}".strip(
                            "-"
                        )
                        + f" [{conn.source_terminal}]"
                    )
                    destination = (
                        f"{conn.destination_component}-{conn.destination_terminal_block}".strip(
                            "-"
                        )
                        + f" [{conn.destination_terminal}]"
                    )
                    writer.writerow([source, destination])
            print("Successfully exported cables")
        except FileNotFoundError:
            logger.info(f"Error: Directory '{file_path}' not found")
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{file_path}'")
        except Exception as e:
            logger.info(f"Error: {e}")
