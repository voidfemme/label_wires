from typing import Tuple
from tkinter import ttk
from typing import TYPE_CHECKING
import tkinter as tk
import logging

from src.ui.localized_widgets import LocalizedButton, LocalizedTreeview

if TYPE_CHECKING:
    from src.controllers.controller import Controller
    from src.event_system import EventSystem
    from src.connection import Connection

logger = logging.getLogger(__name__)


class TreeWidgetFrame(tk.Frame):
    """
    Class that handles the frame that contains the list of wires, and the edit and delete buttons
    """

    def __init__(
        self, parent, controller: "Controller", event_system: "EventSystem", **kwargs
    ):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self._event_system = event_system
        self.keyword_args = kwargs

        # Subscribe to event system events
        self._event_system.subscribe("connection_added", self.on_connection_added)
        self._event_system.subscribe("connection_removed", self.on_connection_removed)

        self.controller.connection_manager.add_observer(self)

        self.connections_dict = {}  # holds list of connections in the treewidget
        self.tree_item_to_connection = {}  # list of items & IDs in the treewidget
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
            self,
            self.controller.localizer,
            "delete",
            command=self.on_delete_button_clicked,
        )
        self.edit_button = LocalizedButton(
            self, self.controller.localizer, "edit", command=self.on_edit_button_clicked
        )

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
            self, self.controller.localizer, self.columns_keys_mapping, show="headings"
        )

        # Callback function to bind selecting an item to the selected connections
        tree.bind("<<TreeviewSelect>>", self.update_selected_connections)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree["yscrollcommand"] = scrollbar.set  # Link the scrollbar to the treeview

        return tree

    # Move this function to the controller, on_delete_button_clicked should call the delete_
    # _connection method from the Controller
    def on_delete_button_clicked(self):
        self.controller.delete_connection_command()

    def on_edit_button_clicked(self):
        self.controller.edit_connection_command()

    def on_connection_added(self, connection):
        # Extract the source and destination tuple to add to the treewidget
        source, destination = self.controller.connection_manager.get_connection_tuple(
            connection
        )

        # Add to tree widget and get unique identifier
        self.item = self.tree_widget.insert("", "end", values=(source, destination))

        # Check if the item was successfully added
        if self.item in self.tree_widget.get_children():
            print(f"Item with ID {self.item} successfully added to the tree widget")
        else:
            print(f"Failed to add item with ID {self.item} to tree widget.")

        # Add to the mapping dictionary
        connection_id = connection.connection_id
        self.tree_item_to_connection[self.item] = (connection_id, connection)

        # Print a message to the UI
        self.parent.display_status(
            self.controller.localizer.get("added_connection").format(
                source=source, destination=destination
            )
        )

        print(f"Added item with ID {self.item} for connection {type(connection)}")
        # Update the tree widget
        self.controller.load_connections()
        self.update_connection_list()
        print("List of wires with their associated IDs:")
        for item_id, conn in self.tree_item_to_connection.items():
            print(f"ID: {item_id}, Connection:{conn}")

    def on_connection_removed(self, connection: "Connection"):
        tree_item = next(
            (
                key
                for key, value in self.tree_item_to_connection.items()
                if value == connection
            ),
            None,
        )

        if tree_item and tree_item in self.tree_widget.get_children():
            self.tree_widget.delete(tree_item)
            del self.tree_item_to_connection[tree_item]
        self.update_connection_list()

    def update_connection_list(self) -> None:
        """
        Update the connection list in the tree widget.
        """
        # Ensure the parent is not in the process of being destroyed
        if not self.parent.is_destroying:
            # Backup the current tree_item_to_connection dictionary
            old_tree_item_to_connection = self.tree_item_to_connection.copy()

            # Clear the current tree widget
            for i in self.parent.tree_widget.get_children():
                self.parent.tree_widget.delete(i)

            # Retrieve the updated list of connections
            connections = self.controller.connection_manager.get_connections()

            # Reset the tree_item_to_connection dictionary since we're repopulating
            self.tree_item_to_connection = {}

            # Populate the tree widget and update the dictionaries

            for connection in connections:
                (
                    source,
                    destination,
                ) = self.controller.connection_manager.get_connection_tuple(connection)
                item_id = self.tree_widget.insert(
                    "", "end", values=(source, destination)
                )

                # Check if this connection had a previous tree item ID in the old dictionary
                old_tree_item = next(
                    (
                        key
                        for key, conn_obj in old_tree_item_to_connection.items()
                        if conn_obj == connection
                    ),
                    None,
                )

                # Use the old tree item ID if available, otherwise use the new ID
                if old_tree_item:
                    self.tree_item_to_connection[old_tree_item] = connection
                else:
                    self.tree_item_to_connection[item_id] = connection

                # Update the connections_dict
                self.connections_dict[str(connection)] = connection

    def update_selected_connections(self, event) -> None:
        # Get currently selected items
        selected_items = self.tree_widget.selection()

        # Clear the selected connections list
        self.selected_connections = []

        # Add all currently selected connections to the list
        for item in selected_items:
            connection = self.tree_item_to_connection.get(item)
            if connection:
                self.selected_connections.append(connection)

        logger.info(f"self.parent.selected_connections = {self.selected_connections}")
