from typing import Tuple
from tkinter import ttk
import tkinter as tk
import logging

from src.localized_widgets import LocalizedButton, LocalizedTreeview
from src.command import DeleteConnectionCommand, EditConnectionCommand

logger = logging.getLogger(__name__)


class TreeWidgetFrame(tk.Frame):
    """
    Class that handles the frame that contains the list of wires, and the edit and delete buttons
    """

    def __init__(
        self,
        parent,
        localizer,
        settings,
        connection_manager,
        command_manager,
        event_system,
        **kwargs,
    ):
        super().__init__(parent)
        self.parent = parent
        self.localizer = localizer
        self.settings = settings
        self.connection_manager = connection_manager
        self.command_manager = command_manager
        self._event_system = event_system

        # Subscribe to event system events
        self._event_system.subscribe("connection_added", self.on_connection_added)
        self._event_system.subscribe("connection_removed", self.on_connection_removed)

        self.connection_manager.add_observer(self)

        self.connections_dict = {}  # holds list of connections in the treewidget
        self.tree_item_to_connection = {}  # What is this for?
        self.selected_connections = []  # user-selected connections
        self.tree_widget = self.create_tree_widget()

        # Create the Button Frame
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Add buttons to the button frame
        self.create_and_place_buttons()

        # Place the tree widget in the grid layout
        self.tree_widget.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        # Configure the grid to expand correctly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Instantiate business logic (temporary)
        self.business_logic = TreeWidgetBusinessLogic(self)

    # Wrapper Functions
    def delete(self, *args, **kwargs):
        self.tree_widget.delete(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self.tree_widget.insert(*args, **kwargs)

    def get_children(self, *args, **kwargs) -> Tuple[str, ...]:
        return self.tree_widget.get_children(*args, **kwargs)

    def selection(self):
        return self.tree_widget.selection()

    def yview_moveto(self, *args, **kwargs):
        # Scrolls to the specified index in the treewidget
        self.tree_widget.yview_moveto(*args, **kwargs)

    # Other Functions
    def create_and_place_buttons(self):
        self.delete_button = LocalizedButton(
            self, self.localizer, "delete", command=self.on_delete_button_clicked
        )
        self.edit_button = LocalizedButton(self, self.localizer, "edit")

        # Pack the buttons into the frame
        self.edit_button.grid(row=1, column=0, sticky=tk.W + tk.E)  # Left
        self.delete_button.grid(row=1, column=1, sticky=tk.W + tk.E)  # Right

        # Fill available space in the cell
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

    def create_tree_widget(self) -> LocalizedTreeview:
        columns = ("#1", "#2")
        columns_keys = ["source", "destination"]
        self.columns_keys_mapping = dict(zip(columns, columns_keys))
        tree = LocalizedTreeview(
            self, self.localizer, self.columns_keys_mapping, show="headings"
        )

        # Callback function to bind selecting an item to the selected connections
        tree.bind("<<TreeviewSelect>>", self.update_selected_connections)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree["yscrollcommand"] = scrollbar.set  # Link the scrollbar to the treeview

        return tree

    def update_selected_connections(self, event) -> None:
        self.business_logic.update_selected_connections(self)
        # print(event)
        # # Get currently selected items
        # selected_items = self.tree_widget.selection()
        #
        # # Clear the selected connections list
        # self.selected_connections = []
        #
        # # Add all currently selected connections to the list
        # for item in selected_items:
        #     connection = self.tree_item_to_connection.get(item)
        #     if connection:
        #         self.selected_connections.append(connection)
        #
        # logger.info(f"self.selected_connections = {self.selected_connections}")

    def on_delete_button_clicked(self):
        command = DeleteConnectionCommand(self)
        self.command_manager.execute(command)
        self.update_connection_list()

    def on_edit_button_clicked(self):
        # First, make sure only one item was selected.

        # Then, populate the fields with the item's values.

        # Use an EditConnectionCommand in order to be able to re-add the old connection
        # command = EditConnectionCommand(self, source, destination, item)
        pass

    def on_connection_added(self, connection):
        # Extract the source and destination tuple to add to the treewidget
        source, destination = self.connection_manager.get_connection_tuple(connection)

        # Add to tree widget and get unique identifier
        self.item = self.tree_widget.insert("", "end", values=(source, destination))

        # Add to the mapping dictionary
        self.tree_item_to_connection[self.item] = connection

        # Print a message to the UI
        self.parent.display_status(
            self.localizer.get("added_connection").format(
                source=source, destination=destination
            )
        )

        # Update the tree widget
        self.business_logic.update_connection_list()

    def on_connection_removed(self, connection):
        item = [k for k, v in self.tree_item_to_connection.items() if v == connection][
            0
        ]
        self.tree_widget.delete(item)
        del self.tree_item_to_connection[item]

    def update_connection_list(self) -> None:
        self.business_logic.update_connection_list()


class TreeWidgetBusinessLogic:
    """
    This class is for refactoring later. The idea is to separate all the business logic into
    this function.
    """

    def __init__(self, parent) -> None:
        self.parent = parent

    def update_connection_list(self) -> None:
        for i in self.parent.tree_widget.get_children():
            self.parent.tree_widget.delete(i)

        connections = self.parent.connection_manager.get_connections()

        for connection in connections:
            source, destination = self.parent.connection_manager.get_connection_tuple(
                connection
            )
            item_id = self.parent.tree_widget.insert(
                "", "end", values=(source, destination)
            )

            self.parent.connections_dict[str(connection)] = connection
            self.parent.tree_item_to_connection[item_id] = connection

    def update_selected_connections(self, event) -> None:
        print(event)
        # Get currently selected items
        selected_items = self.parent.tree_widget.selection()

        # Clear the selected connections list
        self.parent.selected_connections = []

        # Add all currently selected connections to the list
        for item in selected_items:
            connection = self.parent.tree_item_to_connection.get(item)
            if connection:
                self.parent.selected_connections.append(connection)

        logger.info(
            f"self.parent.selected_connections = {self.parent.selected_connections}"
        )
