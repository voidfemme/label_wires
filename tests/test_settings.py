import unittest
from unittest.mock import MagicMock, mock_open, patch
from src.settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Settings()
        self.settings.loaded_settings = {
            "setting_one": "test_one",
            "setting_two": "test_two",
        }

    def test_load_settings(self):
        with patch(
            "json.load", return_value=self.settings.loaded_settings
        ) as mock_json_load:
            with patch("pathlib.Path.open", new_callable=MagicMock):
                self.settings.load_settings()
                mock_json_load.assert_called_once()

    def test_save_settings(self):
        with patch(
            "json.dump", return_value=self.settings.loaded_settings
        ) as mock_json_save:
            with patch("pathlib.Path.open", new_callable=MagicMock):
                self.settings.save_settings()
                mock_json_save.assert_called_once()

    def test_get(self):
        result = self.settings.get("setting_one")
        self.assertEqual(result, "test_one")

    def test_get_default(self):
        # If the setting doesn't exist, `default_value` will returned as the answer
        result = self.settings.get("setting_three", default_value="default test")
        self.assertEqual(result, "default test")

    def test_set(self):
        self.settings.set("setting_one", "urmom")
        self.assertEqual(self.settings.loaded_settings["setting_one"], "urmom")
