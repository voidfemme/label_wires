import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

"""
Singleton class for localization. This class is a singleton in order to allow every Localized
widget to access the same instance of the class. This is important because this allows us to live
update the locale without having to restart the application.

"""

logger = logging.getLogger(__name__)


class LocaleNotFoundError(Exception):
    pass


class LocalizationKeyError(Exception):
    pass


class SingletonMeta(type):
    _instances: Dict[Tuple[Any, ...], Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if args not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[args] = instance
        return cls._instances[args]


class Localizer(metaclass=SingletonMeta):
    def __init__(self, locale: str, default_english=True) -> None:
        self.locale = locale
        self.default_english = default_english
        self.strings = {}
        self.fallback_strings = {}
        self.load_locale()

    def load_locale(self):
        base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))

        logger.info(f"Loading locale: {self.locale}")
        if self.default_english:
            # Load the fallback locale first
            fallback_locale_path = base_path.joinpath("locales", "en.json")
            logger.info(f"Loading fallback locale: {fallback_locale_path}")
            if not fallback_locale_path.exists():
                raise LocaleNotFoundError(
                    "No locale file found for fallback locale 'en'"
                )
            with open(fallback_locale_path, "r", encoding="utf8") as f:
                self.fallback_strings = json.load(f)

        # Then load the desired locale
        locale_path = base_path.joinpath("locales", f"{self.locale}.json")
        if not locale_path.exists():
            raise LocaleNotFoundError(f"No locale file found for {self.locale}")
        with open(locale_path, "r", encoding="utf-8") as f:
            self.strings = json.load(f)

    def get(self, key: str) -> str:
        if key not in self.strings:
            if self.default_english and key in self.fallback_strings:
                return self.fallback_strings[key]
            else:
                raise LocalizationKeyError(f'No localization for key "{key}"')
        return self.strings[key]

    def set_locale(self, new_locale: str) -> None:
        self.locale = new_locale
        logger.info(f"Setting locale to: {self.locale}")
        self.load_locale()
