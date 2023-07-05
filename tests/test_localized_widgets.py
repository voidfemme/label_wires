import unittest
from unittest.mock import patch, MagicMock
from src.localized_widgets import (
    LocalizedLabel,
    LocalizedButton,
    LocalizedCheckButton,
    LocalizedCombobox,
    LocalizedTreeview,
)


class TestLocalizedLabel(unittest.TestCase):
    def setUp(self):
        self.localizer = MagicMock()
        self.master = MagicMock()
        self.l10n_key = "hello"
        self.format_args = {}
        self.localized_label = LocalizedLabel(
            self.master, self.localizer, self.l10n_key, self.format_args
        )

    def test_get_localized_text(self):
        self.localizer.get.return_value = "Hello"
        text = self.localized_label.get_localized_text()
        self.assertEqual(text, "Hello")

    def test_update_format_args(self):
        new_format_args = {"arg1": "value1"}
        self.localized_label.update_format_args(new_format_args)
        self.assertEqual(self.localized_label.format_args, new_format_args)

    def test_update(self):
        self.localizer.get.return_value = "Updated Text"
        self.localized_label.update()
        self.master.config.assert_called_once_with(text="Updated Text")

    def test_destroy(self):
        self.assertIn(self.localized_label, LocalizedLabel._all_instances)
        self.localized_label.destroy()
        self.assertNotIn(self.localized_label, LocalizedLabel._all_instances)

    def test_update_all(self):
        localizer2 = MagicMock()
        l10n_key2 = "goodbye"
        format_args2 = {}
        localized_label2 = LocalizedLabel(
            self.master, localizer2, l10n_key2, format_args2
        )

        LocalizedLabel.update_all()

        self.master.config.assert_called()  # Verify that config was called
        self.assertEqual(
            self.master.config.call_count, 2
        )  # It should have been called twice (once for each instance)

        localized_label2.destroy()  # Clean up


class TestLocalizedButton(unittest.TestCase):
    def setUp(self):
        self.localizer = MagicMock()
        self.master = MagicMock()
        self.l10n_key = "hello"
        self.format_args = {}
        self.localized_button = LocalizedButton(
            self.master, self.localizer, self.l10n_key, self.format_args
        )

    def test_get_localized_text(self):
        self.localizer.get.return_value = "Hello"
        text = self.localized_button.get_localized_text()
        self.assertEqual(text, "Hello")

    def test_update_format_args(self):
        new_format_args = {"arg1": "arg2"}
        self.localized_button.update_format_args(new_format_args)
        self.assertEqual(self.localized_button.format_args, new_format_args)

    def test_update(self):
        self.localizer.get.return_value("Hello world")
        self.localized_button.update()
        self.master.config.assert_called_once_with(text="Hello World")

    def test_destroy(self):
        self.assertIn(self.localized_button, LocalizedButton._all_instances)
        self.localized_button.destroy()
        # Check to make sure it got deleted from the array of instances
        self.assertNotIn(self.localized_button, LocalizedButton._all_instances)

    def test_update_all(self):
        localizer2 = MagicMock()
        l10n_key2 = "goodbye"
        format_args2 = {}
        localized_button2 = LocalizedButton(
            self.master, localizer2, l10n_key2, format_args2
        )

        LocalizedButton.update_all()
        self.master.assert_called()
        self.assertEqual(self.master.config.call_count, 2)

        localized_button2.destroy()


class TestLocalizedCheckButton(unittest.TestCase):
    def setUp(self):
        self.localizer = MagicMock()
        self.master = MagicMock()
        self.l10n_key = "hello"
        self.format_args = {}
        self.localized_check_button = LocalizedCheckButton(
            self.master, self.localizer, self.l10n_key, self.format_args
        )

    def test_get_localized_text(self):
        self.localizer.get.return_value("Hello")
        text = self.localized_check_button.get_localized_text()
        self.assertEqual(text, "Hello")

    def test_update_format_args(self):
        new_format_args = {"arg1": "arg2"}
        self.localized_check_button.update_format_args(new_format_args)
        self.assertEqual(self.format_args, new_format_args)

    def test_update(self):
        self.localizer.get.return_value("Hello world")
        self.localized_check_button.update()
        self.master.config.assert_called_once_with(text="Hello world")

    def test_destroy(self):
        self.assertIn(self.localized_check_button, LocalizedCheckButton._all_instances)
        self.localized_check_button.destroy()
        self.assertNotIn(
            self.localized_check_button, LocalizedCheckButton._all_instances
        )

    def test_update_all(self):
        localizer2 = MagicMock()
        l10n_key2 = "goodbye"
        format_args2 = {}
        localized_check_button2 = LocalizedCheckButton(
            self.master, localizer2, l10n_key2, format_args2
        )

        LocalizedCheckButton.update_all()
        self.master.assert_called()
        self.assertEqual(self.master.config.call_count, 2)

        localized_check_button2.destroy()


class TestLocalizedCombobox(unittest.TestCase):
    def setUp(self):
        self.master = MagicMock()
        self.localizer = MagicMock()
        self.values_key = "setUp values_key"
        self.localizer.get.return_value = ["Option 1", "Option 2"]

    @patch("tkinter.ttk.Combobox.__init__")
    def test_init(self, mock_super_init):
        localized_combobox = LocalizedCombobox(
            self.master, self.localizer, self.values_key
        )

        mock_super_init.assert_called_once_with(
            self.master, values=self.localizer.get.return_value
        )

        self.assertEqual(len(localized_combobox._all_instances), 1)

    def test_update(self):
        values_key2 = "test_update values_key2"
        localized_combobox2 = LocalizedCombobox(
            self.master, self.localizer, values_key2
        )

        # Simulate a change in the localization values
        self.localizer.get.return_value = ["new", "values"]
        localized_combobox2.update()
        localized_combobox2.config.assert_called_once_with(
            values=self.localizer.get.return_value
        )

    def test_destroy(self):
        values_key3 = "test_destroy values_key3"
        localized_combobox3 = LocalizedCombobox(
            self.master, self.localizer, values_key3
        )
        self.assertIn(localized_combobox3, LocalizedCombobox._all_instances)
        localized_combobox3.destroy()
        self.assertNotIn(localized_combobox3, LocalizedCombobox._all_instances)

    @patch.object(LocalizedCombobox, "update")
    def test_update_all(self):
        localized_combobox4 = LocalizedCombobox(
            self.master, self.localizer, self.values_key
        )
        localized_combobox5 = LocalizedCombobox(
            self.master, self.localizer, self.values_key
        )
        LocalizedCombobox.update_all()
        self.master.assert_called()
        self.assertEqual(self.master.config.call_count, 2)

        localized_combobox4.destroy()
        localized_combobox5.destroy()


class TestLocalizedTreeview(unittest.TestCase):
    def setUp(self):
        self.master = MagicMock()
        self.localizer = MagicMock()
        columns = ("#1", "#2")
        columns_keys = ["test col 1", "test col 2"]
        self.columns_keys_mapping = dict(zip(columns, columns_keys))

    @patch.object(LocalizedTreeview, "update")
    @patch("tkinter.ttk.Treeview")
    def test_init(self, mock_super_init, mock_update):
        localized_treeview = LocalizedTreeview(
            self.master, self.localizer, self.columns_keys_mapping
        )
        mock_super_init.assert_called_once_with(
            self.master,
            columns=list(self.columns_keys_mapping.keys()),
            values=self.localizer.get.return_value,
        )

        self.assertEqual(len(localized_treeview._all_instances), 1)

    def test_update(self):
        columns2 = ("#1", "#2")
        columns_keys2 = ["update col 1", "update col 2"]
        columns_keys_mapping2 = dict(zip(columns2, columns_keys2))
        localized_treeview2 = LocalizedTreeview(
            self.master, self.localizer, columns_keys_mapping2
        )

        # Simulate a change in the localization values
        self.localizer.get.return_value = ["new", "values"]

        for column in columns2:
            with patch.object(localized_treeview2, "heading") as mock_heading:
                localized_treeview2.update()
                mock_heading.assert_called_once_with(
                    column, text=self.localizer.get.return_value
                )

    def test_destroy(self):
        columns3 = ("#1", "#2")
        columns_keys3 = ["test destroy 1", "test destroy 2"]
        columns_keys_mapping3 = dict(zip(columns3, columns_keys3))
        localized_treeview3 = LocalizedTreeview(
            self.master, self.localizer, columns_keys_mapping3
        )
        self.assertIn(localized_treeview3, LocalizedTreeview._all_instances)
        localized_treeview3.destroy()
        self.assertNotIn(localized_treeview3, LocalizedTreeview._all_instances)

    @patch.object(LocalizedTreeview, "update")
    def test_update_all(self, mock_update):
        columns4 = ("#1", "#2")
        columns_keys4 = ["update_all col 1", "update_all col 2"]
        columns_keys_mapping4 = dict(zip(columns4, columns_keys4))
        localized_treeview4 = LocalizedTreeview(
            self.master, self.localizer, columns_keys_mapping4
        )

        columns_keys_5 = ["udpate_all col 3", "update_all col 4"]
        columns_keys_mapping5 = dict(zip(columns4, columns_keys_5))
        localized_treeview5 = LocalizedTreeview(
            self.master, self.localizer, columns_keys_mapping5
        )

        LocalizedTreeview.update_all()
        assert mock_update.call_count == 2

        localized_treeview4.destroy()
        localized_treeview5.destroy()


if __name__ == "__main__":
    unittest.main()
