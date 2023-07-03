import json
from pathlib import Path


class LocaleNotFoundError(Exception):
    pass


class LocalizationKeyError(Exception):
    pass


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if args not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[args] = instance
        return cls._instances[args]


class Localizer(metaclass=SingletonMeta):
    def __init__(self, locale, default_english=True):
        self.locale = locale
        self.default_english = default_english
        self.strings = {}
        self.fallback_strings = {}
        self.load_locale()

    def load_locale(self):
        print("------------------------------")
        print(f"Loading locale: {self.locale}")
        if self.default_english:
            # Load the fallback locale first
            fallback_locale_path = Path("locales") / "en.json"
            if not fallback_locale_path.exists():
                raise LocaleNotFoundError(
                    "No locale file found for fallback locale 'en'"
                )
            with fallback_locale_path.open("r") as f:
                self.fallback_strings = json.load(f)

        # Then load the desired locale
        locale_path = Path("locales") / f"{self.locale}.json"
        if not locale_path.exists():
            raise LocaleNotFoundError(f"No locale file found for {self.locale}")
        with locale_path.open("r") as f:
            self.strings = json.load(f)

        # print(f"Loaded strings for {self.locale}: {self.strings}")
        # print(f"Loaded fallback_strings: {self.fallback_strings}")

    def get(self, key):
        if key not in self.strings:
            if self.default_english and key in self.fallback_strings:
                return self.fallback_strings[key]
            else:
                raise LocalizationKeyError(f'No localization for key "{key}"')
        return self.strings[key]

    def set_locale(self, new_locale):
        self.locale = new_locale
        print(f"Setting locale to: {self.locale}")
        self.load_locale()
