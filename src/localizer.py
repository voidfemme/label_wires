# localizer.py
import json
from pathlib import Path


class LocaleNotFoundError(Exception):
    pass


class LocalizationKeyError(Exception):
    pass


class Localizer:
    def __init__(self, locale):
        self.locale = locale
        self.strings = {}
        self.load_locale()

    def load_locale(self):
        locale_path = Path("locales") / f"{self.locale}.json"
        if not locale_path.exists():
            raise LocaleNotFoundError(f"No locale file found for {self.locale}")

        with locale_path.open("r") as f:
            self.strings = json.load(f)

    def get(self, key):
        if key not in self.strings:
            raise LocalizationKeyError(f'No localization for key "{key}"')
        return self.strings[key]
