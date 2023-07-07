import unittest
import src.validation as validation


class TestIsValidEntryString(unittest.TestCase):
    def test_is_string_a_string(self):
        invalid_input_int = 50
        test_result = validation.is_valid_entry_string(invalid_input_int)
        self.assertFalse(test_result)

        self.assertTrue

    def test_is_string_printable(self):
        invalid_input_string = "test string with \t non-printable character"
        test_result = validation.is_valid_entry_string(invalid_input_string)
        self.assertFalse(test_result)

    def test_is_string_printable_and_a_string(self):
        valid_input = "This is some valid test input!"
        test_result = validation.is_valid_entry_string(valid_input)
        self.assertTrue(test_result)


class TestValidateJSONData(unittest.TestCase):
    def test_is_data_string(self):
        invalid_json_string = ""
