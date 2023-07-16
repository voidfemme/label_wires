import logging
import json
from src.connection import Connection

logger = logging.getLogger(__name__)


class FileHandler:
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path

    def load(self):
        if not self.file_path:
            return
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            logger.info(f"Error, {self.file_path} not found. Creating a new file")
            with open(self.file_path, "w"):
                return None
        except PermissionError:
            logger.info(f"Error: Permission denied to read from'{self.file_path}'")
            return None
        except ValueError:
            logger.info(
                f"Error: Invalid JSON data. Please inspect the input file: {self.file_path}"
            )
            return None
        except Exception as e:
            logger.info(f"Error loading JSON file: {e}")
            return None

    def save(self, data: list[dict[str, str]]):
        if not self.file_path:
            return False
        try:
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except FileNotFoundError:
            logger.info(f"Error: File {self.file_path} not found.")
            return False
        except PermissionError:
            logger.info(f"Permission Error: could not write to: {self.file_path}")
            return False
        except ValueError:
            logger.info("ValueError: Could not write data to file.")
            return False
        except Exception as e:
            logger.info(f"Error: {e}")
            return False

    def export(self, format, data):
        pass

    def validate_json_wire_fields(self, input_data: list[dict[str, str]]):
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
