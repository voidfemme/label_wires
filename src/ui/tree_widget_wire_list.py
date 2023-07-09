from typing import Tuple
from tkinter import ttk
import tkinter as tk

from src.localized_widgets import LocalizedButton, LocalizedTreeview


class TreeWidgetFrame(tk.Frame):
    def __init__(
        self, parent, localizer, settings, connection_manager, command_manager, **kwargs
    ):
        super().__init__(parent)
        self.parent = parent
        self.localizer = localizer
        self.settings = settings
        self.connection_manager = connection_manager
        self.command_manager = command_manager

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
        self.tree_widget.yview_moveto(*args, **kwargs)

    def call_parent_method(self, method_name, *args, **kwargs):
        method = getattr(self.parent, method_name, None)
        if method:
            return method(*args, **kwargs)
        else:
            raise AttributeError(f"No such method: {method_name}")

    def get_parent_attribute(self, attribute_name):
        attribute = getattr(self.parent, attribute_name, None)
        if attribute is None:
            raise AttributeError(f"No such attribute: {attribute_name}")
        return attribute

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

        tree.bind("<<TreeviewSelect>>", self.parent.update_selected_connections)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree["yscrollcommand"] = scrollbar.set  # Link the scrollbar to the treeview

        return tree

    def on_delete_button_clicked(self):
        self.parent.handle_delete_button_clicked()
