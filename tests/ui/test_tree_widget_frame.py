import tkinter as tk
import unittest
import _tkinter

from unittest.mock import Mock, MagicMock

from src.ui.tree_widget_frame import TreeWidgetFrame


class TKinterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tk.Tk()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        # Manually "pump" through the events in the tkinter gui
        # taken from: https://stackoverflow.com/questions/4083796/how-do-i-run-unittest-on-a-tkinter-app
        # by user ivan_pozdeev on Feb 28, 2018
        while self.root.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
            pass


class TestTreeWidgetFrame(TKinterTestCase):
    def setUp(self):
        super().setUp()
        self.localizer = Mock()
        self.settings = Mock()
        self.connection_manager = Mock()
        self.command_manager = Mock()

        self.tree_widget_frame = TreeWidgetFrame(
            self.root,
            self.localizer,
            self.settings,
            self.connection_manager,
            self.command_manager,
        )

        # Pay close attention that we are mocking the methods of the Treewidget itself,
        # not the tree_widget_frame
        self.tree_widget_frame.tree_widget.delete = Mock()
        self.tree_widget_frame.tree_widget.insert = Mock()
        self.tree_widget_frame.tree_widget.get_children = Mock()
        self.tree_widget_frame.tree_widget.selection = Mock()
        self.tree_widget_frame.tree_widget.yview_moveto = Mock()
        self.tree_widget_frame.tree_widget.selection = MagicMock()

    def test_delete(self):
        self.tree_widget_frame.delete("test item")
        self.pump_events()
        self.tree_widget_frame.tree_widget.delete.assert_called_once_with("test item")

    def test_insert(self):
        self.tree_widget_frame.insert("", "end", values=("test item 2", "test item 3"))
        self.pump_events()
        self.tree_widget_frame.tree_widget.insert.assert_called_once_with(
            "", "end", values=("test item 2", "test item 3")
        )

    def test_get_children(self):
        self.tree_widget_frame.get_children()
        self.tree_widget_frame.tree_widget.get_children.assert_called_once()

    def test_selection(self):
        self.tree_widget_frame.selection()
        self.tree_widget_frame.tree_widget.selection.assert_called_once()

    def test_yview_moveto(self):
        self.tree_widget_frame.yview_moveto()
        self.tree_widget_frame.tree_widget.yview_moveto.assert_called_once()

    def test_update_selected_connections(self):
        mock_event = Mock()
        self.tree_widget_frame.update_selected_connections(mock_event)

