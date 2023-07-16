import unittest
from unittest.mock import Mock, patch
from src.controllers.controller import Controller


class TestController(unittest.TestCase):
    # 1. If no items are selected, the method returns early
    # 2. If a connection is selected, the method gets the old connection
    #    and populates the entry boxes in the view with the old values
    # 3. It then gets the new values from the entry boxes in the View.
    # 4. Finally, it creates and executes an EditConnectionCommand
    def setUp(self) -> None:
        self.controller = Controller()
        self.controller.view = Mock()
        self.controller.view.tree_widget = Mock()
        self.controller.view.connection_entry_frame = Mock()
        self.controller.command_manager = Mock()

    @patch("controller.EditConnectionCommand")
    def test_edit_connection_no_items_deleted(self, MockEditConnectionCommand):
        # If no items are selected, the method returns early
        self.controller.view.tree_widget.selection.return_value = []

        self.controller.edit_connection()

        self.controller.view.tree_widget.selection.assert_called_once()
        MockEditConnectionCommand.assert_not_called()
        self.controller.command_manager.execute.assert_not_called()

    @patch("controller.EditConnectionCommand")
    def test_edit_connection_item_selected(self, MockEditConnectionCommand):
        self.controller.view.tree_widget.selection.return_value = ["item1"]
        self.controller.view.tree_widget.tree_item_to_connection = {
            "item1": "old_connection"
        }
        self.controller.view.connection_entry_frame.source_component.get.return_value = (
            "new_source_component"
        )
        self.controller.view.connection_entry_frame.source_terminal_block.get.return_value = (
            "new_source_terminal_block"
        )
        self.controller.view.connection_entry_frame.source_terminal.get.return_value = (
            "new_source_terminal"
        )
        self.controller.view.connection_entry_frame.destination_component.get.return_value = (
            "new_destination_component"
        )
        self.controller.view.connection_entry_frame.destination_terminal_block.get.return_value = (
            "new_destination_terminal_block"
        )
        self.controller.view.connection_entry_frame.destination_terminal.get.return_value = (
            "new_destination_terminal"
        )

        self.controller.edit_connection()

        self.controller.view.tree_widget.selection.assert_called_once()
        self.controller.view.connection_entry_frame.populate_entries.assert_called_once_with(
            "old_connection"
        )
        MockEditConnectionCommand.assert_called_once()
        self.controller.command_manager.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
