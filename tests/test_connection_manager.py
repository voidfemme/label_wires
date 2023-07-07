import unittest
from src.connection_manager import ConnectionManager


class TestConnectionManager(unittest.TestCase):
    def test_save_to_file(self):
        m = mock_open(read_data="test data")
