import unittest
from unittest.mock import MagicMock
from src.command import Command, EditConnectionCommand, AddConnectionCommand, DeleteConnectionCommand


# The Command class needs to be untangled a little from the gui and the wiremanager. 
class TestAddConnectionCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = MagicMock()

    def test_execute(self):
        pass
