from typing import Type
import unittest
from unittest.mock import MagicMock, mock_open, patch
from src.connection import Connection, Wire, Cable
from pathlib import Path

from src.connection_manager import ConnectionManager, WireManager, CableManager

# Pyright errors can be misleading!


class ConnectionManagerTestClass(ConnectionManager):
    def add_connection(self, *args) -> bool:
        return True

    def get_connection_class(self) -> Type[Connection]:
        return Connection


class TestConnectionManager(unittest.TestCase):
    def setUp(self) -> None:
        self.conn_manager = ConnectionManagerTestClass("/fake/path")
        self.wire_1 = MagicMock()
        self.wire_1.to_dict.return_value = {"mock": "wire1"}  # Side effect
        self.wire_2 = MagicMock()
        self.wire_2.to_dict.return_value = {"mock": "wire2"}  # Side effect
        self.conn_manager.connections = [self.wire_1, self.wire_2]
        self.test_file_path = "test/file/path"

    def tearDown(self) -> None:
        self.conn_manager = None
        self.wire_1 = None
        self.wire_2 = None

    def test_save_json_to_file_open(self):
        with patch("builtins.open", mock_open()) as m:
            self.conn_manager.save_json_to_file()
            m.assert_called_once_with(self.conn_manager.file_path, "w")

    def test_save_json_file_not_found(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = FileNotFoundError
            result = self.conn_manager.save_json_to_file()
            self.assertFalse(result)

    def test_save_json_to_file_permission_error(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = PermissionError
            result = self.conn_manager.save_json_to_file()
            self.assertFalse(result)

    def test_load_json_from_file_open(self):
        with patch("builtins.open", mock_open()) as m:
            self.conn_manager.load_json_from_file()
            m.assert_called_once_with(self.conn_manager.file_path, "r")

    def test_load_json_file_not_found(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = FileNotFoundError
            result = self.conn_manager.save_json_to_file()
            self.assertFalse(result)

    def test_load_json_file_permission_error(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = PermissionError
            result = self.conn_manager.save_json_to_file()
            self.assertFalse(result)

    def test_load_json_file_value_error(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = ValueError
            result = self.conn_manager.save_json_to_file()
            self.assertFalse(result)

    def test_is_valid_entry_string_valid(self):
        valid_input_string = "test string"
        result = self.conn_manager.is_valid_entry_string(valid_input_string)
        self.assertTrue(result)

    def test_is_valid_entry_string_not_string(self):
        invalid_input_num = 5
        result = self.conn_manager.is_valid_entry_string(invalid_input_num)
        self.assertFalse(result)

    def test_is_valid_entry_string_not_printable(self):
        invalid_input_string = "test\x00string"
        result = self.conn_manager.is_valid_entry_string(invalid_input_string)
        self.assertFalse(result)

    def test_validate_json_data_missing_fields(self):
        invalid_json_data = [
            {
                "source_component": "test",
                "source_terminal_block": "test",
                "source_terminal": "test",
                "destination_component": "test",
                "destination_terminal_block": "test",
                "destination_terminal": "test",
            },
            {
                "source_component": "test",
                "source_terminal_block": "test",
                "source_terminal": "test",
                "destination_component": "test",
                "destination_terminal": "test",
            },
        ]
        with self.assertRaises(ValueError):
            self.conn_manager.validate_json_data(invalid_json_data)

    def test_validate_json_data_extra_fields(self):
        invalid_json_data = [
            {
                "source_component": "test",
                "source_terminal_block": "test",
                "source_terminal": "test",
                "destination_component": "test",
                "destination_terminal_block": "test",
                "destination_terminal": "test",
                "destination_terminal": "test",
            },
            {
                "source_component": "test",
                "source_terminal_block": "test",
                "source_terminal": "test",
                "destination_component": "test",
                "destination_terminal": "test",
            },
        ]
        with self.assertRaises(ValueError):
            self.conn_manager.validate_json_data(invalid_json_data)

    def test_validate_json_data_non_string(self):
        invalid_json_data = [
            {
                "source_component": "test",
                "source_terminal_block": "test",
                "source_terminal": "test",
                "destination_component": "test",
                "destination_terminal_block": "test",
                "destination_terminal": "test",
                "destination_terminal": "test",
            },
            {
                "source_component": "test",
                "source_terminal_block": "test",
                "source_terminal": "test",
                "destination_component": 4,
                "destination_terminal": "test",
            },
        ]
        with self.assertRaises(ValueError):
            self.conn_manager.validate_json_data(invalid_json_data)

    def test_validate_json_data_non_list(self):
        invalid_json_data = {
            "source_component": "test",
            "source_terminal_block": "test",
            "source_terminal": "test",
            "destination_component": "test",
            "destination_terminal_block": "test",
            "destination_terminal": "test",
            "destination_terminal": "test",
        }
        with self.assertRaises(ValueError):
            self.conn_manager.validate_json_data(invalid_json_data)  # type: ignore

    def test_delete_connection_valid(self):
        # Arrange
        connection1 = MagicMock()
        connection2 = MagicMock()
        connection3 = MagicMock()
        self.conn_manager.connections.append(connection1)
        self.conn_manager.connections.append(connection2)
        self.conn_manager.connections.append(connection3)

        number_of_connections = len(self.conn_manager.connections)

        # Mock the "save_json_to_file" method
        with patch.object(self.conn_manager, "save_json_to_file") as mock_save:
            result = self.conn_manager.delete_connection(connection2)
            self.assertTrue(result)  # connection2 has been deleted
            self.assertNotIn(
                self.conn_manager.connections, connection2
            )  # Connection two is no longer in the list of connections
            self.assertEqual(
                len(self.conn_manager.connections), number_of_connections - 1
            )  # The list of connections should now be 1 less than what we started with
            mock_save.assert_called_once()

    def test_delete_connection_invalid(self):
        connection1 = MagicMock()
        connection2 = MagicMock()
        connection3 = MagicMock()
        connection4 = MagicMock()
        self.conn_manager.connections.append(connection1)
        self.conn_manager.connections.append(connection2)
        self.conn_manager.connections.append(connection3)

        number_of_connections = len(self.conn_manager.connections)

        with patch.object(self.conn_manager, "save_json_to_file") as mock_save:
            result = self.conn_manager.delete_connection(
                connection4
            )  # deleted connection not in the list
            self.assertFalse(result)  # Did not delete the item
            self.assertEqual(
                len(self.conn_manager.connections), number_of_connections
            )  # The number of connections should stay the same
            mock_save.assert_not_called()  # We don't save because nothing was added to the file

    def test_edit_connection(self):
        # Come back to this one
        pass

    def test_get_connection_tuple_not_exist(self):
        invalid_connection = MagicMock()
        result = self.conn_manager.get_connection_tuple(invalid_connection)
        self.assertEqual(result, ("", ""))

    def test_get_connection_tuple_success(self):
        result = self.conn_manager.get_connection_tuple(self.wire_1)
        self.assertEqual(self.wire_1.to_tuple(), result)

    def test_get_connections(self):
        original_connections = self.conn_manager.connections
        returned_connections = self.conn_manager.get_connections()

        self.assertFalse(original_connections is returned_connections)
        self.assertEqual(original_connections, returned_connections)

    def test_export_to_csv_file_exists(self):
        # Arrange
        test_file_path = "test/file/path"
        self.conn_manager = ConnectionManagerTestClass(test_file_path)

        # Mock the "exists" method of "Path" to always return True
        with patch.object(Path, "exists", return_value=True):
            # Act and Assert
            with self.assertRaises(FileExistsError):
                self.conn_manager.export_to_csv(test_file_path)

    def test_export_to_csv_success(self):
        with patch("builtins.open", mock_open()) as m:
            self.conn_manager.export_to_csv(self.test_file_path)
            m.assert_called_once_with(Path(self.test_file_path), "w", newline="")

    def test_export_to_csv_file_not_found(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = FileNotFoundError
            result = self.conn_manager.export_to_csv(self.test_file_path)
            self.assertFalse(result)

    def test_export_to_csv_permission_error(self):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = PermissionError
            result = self.conn_manager.export_to_csv(self.test_file_path)
            self.assertFalse(result)


class TestWireManager(unittest.TestCase):
    def setUp(self):
        self.wire_manager = WireManager("/fake/path")

    def tearDown(self) -> None:
        self.conn_manager = None

    def test_get_connection_class(self):
        result = self.wire_manager.get_connection_class()
        self.assertEqual(result, Wire)

    def test_add_connection(self):
        result = self.wire_manager.add_connection("f1", "f2", "f3", "f4", "f5", "f6")
        self.assertTrue(result)

        result2 = self.wire_manager.add_connection("f4", "f5", "f6", "f1", "f2", "f3")
        self.assertFalse(result2)


class TestCableManager(unittest.TestCase):
    def setUp(self):
        self.cable_manager = CableManager("/fake/path")

    def tearDown(self) -> None:
        self.conn_manager = None

    def test_get_connection_class(self):
        result = self.cable_manager.get_connection_class()
        self.assertEqual(result, Cable)

    def test_add_connection(self):
        result = self.cable_manager.add_connection("f1", "f2", "f3", "f4", "f5", "f6")
        self.assertTrue(result)

        result2 = self.cable_manager.add_connection("f2", "f2", "f3", "f4", "f5", "f6")
        self.assertFalse(result2)
