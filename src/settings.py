import json
from pathlib import Path


class Settings:
    def __init__(self, file_path=Path("config/settings.json")):
        self.file_path = file_path
        self.settings = {}
        if self.file_path.is_file():
            self.load_settings()

    def load_settings(self):
        with self.file_path.open("r") as f:
            self.settings = json.load(f)

    def save_settings(self):
        with self.file_path.open("w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, setting_key, default=None) -> str:
        return self.settings.get(setting_key, default)

    def set(self, setting_key, setting_value):
        self.settings[setting_key] = setting_value
