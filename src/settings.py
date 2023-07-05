import json
from pathlib import Path

"""
To use this class, you need to create a settings.json file in the config folder.
The settings.json file should look like this:
{
    "language": "en",
    "default_wire_file_directory": "",
    "default_csv_directory": "",
    "default_save_location": "/home/rsp/documents",
    "csv_save_location": "/home/rsp/documents",
    "default_csv_delimiter": "|"
}
Settings can be retrieved by using the get method, passing the setting key as an argument.
"""

class Settings:
    def __init__(self, file_path=None) -> None:
        if file_path is None:
            file_path = Path(__file__).resolve().parent.parent.joinpath("config", "settings.json")
        self.file_path = file_path
        self.settings = {}
        if self.file_path.is_file():
            self.load_settings()

    def load_settings(self) -> None:
        with self.file_path.open("r", encoding="utf-8") as f:
            self.settings = json.load(f)

    def save_settings(self) -> None:
        with self.file_path.open("w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, setting_key, default=None) -> str:
        return self.settings.get(setting_key, default)

    def set(self, setting_key, setting_value) -> None:
        self.settings[setting_key] = setting_value
