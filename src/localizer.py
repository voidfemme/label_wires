import json
from pathlib import Path


class LocaleNotFoundError(Exception):
    pass


class LocalizationKeyError(Exception):
    pass


class Localizer:
    def __init__(self, locale, fallback_to_english=True):
        self.locale = locale
        self.fallback_to_english = fallback_to_english
        self.strings = {}
        self.fallback_strings = {}
        self.load_locale()

    def load_locale(self):
        if self.fallback_to_english:
            # Load the fallback locale first
            fallback_locale_path = Path("locales") / "en.json"
            if not fallback_locale_path.exists():
                raise LocaleNotFoundError("No locale file found for fallback locale 'en'")
            with fallback_locale_path.open("r") as f:
                self.fallback_strings = json.load(f)

        # Then load the desired locale
        locale_path = Path("locales") / f"{self.locale}.json"
        if not locale_path.exists():
            raise LocaleNotFoundError(f"No locale file found for {self.locale}")
        with locale_path.open("r") as f:
            self.strings = json.load(f)

    def get(self, key):
        if key not in self.strings:
            if self.fallback_to_english and key in self.fallback_strings:
                return self.fallback_strings[key]
            else:
                raise LocalizationKeyError(f'No localization for key "{key}"')
        return self.strings[key]

