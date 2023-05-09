import unittest
import os
import csv
from io import StringIO
from unittest.mock import patch
from label_wires.wire_manager import (
    is_valid_input,
    is_valid_destination,
    is_valid_file_name,
    WireManager,
)

WIRENUMS_DIR = os.path.join(os.path.dirname(__file__), "..", "label_wires", "data")


class TestWireManager(unittest.TestCase):
    def test_is_valid_input(self):
        self.assertTrue(is_valid_input("ABC123"))
        self.assertFalse(is_valid_input("ABC 123"))
        self.assertFalse(is_valid_input("!@#$%^"))

    def test_is_valid_destination(self):
        self.assertTrue(is_valid_destination("WIRE-A1"))
        self.assertTrue(is_valid_destination("WIRE-A1-B2"))
        self.assertFalse(is_valid_destination("WIRE-A1-B2-C3-D4-E5"))
        self.assertFalse(is_valid_destination("WIRE-A1!"))

    def test_is_valid_file_name(self):
        self.assertTrue(is_valid_file_name("test_file"))
        self.assertFalse(is_valid_file_name("test<>file"))
        self.assertFalse(is_valid_file_name("test\\|?*file"))

    def test_WireManager_init(self):
        wm = WireManager("test", WIRENUMS_DIR)
        self.assertEqual(wm.csv_file_name, "test")
        self.assertEqual(
            wm.output_dir,
            os.path.join(os.path.dirname(__file__), "..", "label_wires", "data"),
        )
        self.assertEqual(wm.wires, [])

    def test_WireManager_is_duplicate_or_reverse(self):
        wm = WireManager("test", WIRENUMS_DIR)
        wm.wires = [("A-B-C", "D"), ("D", "A-B-C")]

        self.assertTrue(wm.is_duplicate_or_reverse(("A-B-C", "D")))
        self.assertTrue(wm.is_duplicate_or_reverse(("D", "A-B-C")))
        self.assertFalse(wm.is_duplicate_or_reverse(("X-Y-Z", "D")))

    @patch("builtins.input", side_effect=["C1", "TB1", "T1", "EE-343-1A", "", "", "quit"])
    def test_WireManager_gather_input(self, mock_input):
        wm = WireManager("test", WIRENUMS_DIR)
        with patch("sys.stdout", new=StringIO()) as mock_output:
            wm.gather_input()
        output = mock_output.getvalue()
        self.assertIn("Added: C1-TB1-T1, EE-343-1A", output)
        self.assertIn(('C1-TB1-T1', 'EE-343-1A'), wm.wires)

    # Additional tests for WireManager methods:

    def test_WireManager_save_to_csv(self):
        wm = WireManager("test", WIRENUMS_DIR)
        wm.wires = [("A-B-C", "D"), ("D", "A-B-C")]

        with patch("sys.stdout", new=StringIO()) as mock_output:
            wm.save_to_csv()

        output = mock_output.getvalue()
        self.assertIn("CSV file saved as", output)

        # Check that the file has been saved with the correct content
        file_name = output.split()[-1]
        file_path = os.path.join(WIRENUMS_DIR, file_name)
        with open(file_path, "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            rows = [tuple(row) for row in csv_reader]
        self.assertEqual(rows, wm.wires)

        # Clean up the created test file
        os.remove(file_path)

    def test_WireManager_load_from_csv(self):
        wm = WireManager("test", WIRENUMS_DIR)

        # Save a CSV file to load
        wm.wires = [("A-B-C", "D"), ("D", "A-B-C")]
        with patch("sys.stdout", new=StringIO()) as mock_output:
            wm.save_to_csv()
        output = mock_output.getvalue()
        file_name = output.split()[-1]
        file_path = os.path.join(WIRENUMS_DIR, file_name)

        # Load the previously saved CSV file
        wm2 = WireManager("test", WIRENUMS_DIR)
        with patch("builtins.input", side_effect=["1"]):
            with patch("sys.stdout", new=StringIO()) as mock_output:
                wm2.load_from_csv()
            output = mock_output.getvalue()
        self.assertIn("Loaded 2 existing wire connections", output)

        # Check that the wires have been loaded correctly
        self.assertEqual(wm2.wires, wm.wires)

        # Clean up the created test file
        os.remove(file_path)

    def test_WireManager_filter_wires(self):
        wm = WireManager("test", WIRENUMS_DIR)
        wm.wires = [
            ("C2-TB1-T1", "D1"),
            ("C1-TB2-T2", "D2"),
            ("C1-TB1-T1", "D1"),
        ]

        filtered_wires = wm.filter_wires("component", "C1")
        self.assertEqual(
            filtered_wires,
            [
                ("C1-TB2-T2", "D2"),
                ("C1-TB1-T1", "D1"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
