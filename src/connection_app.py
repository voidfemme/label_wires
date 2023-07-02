# Love is love. Be yourself
import json
import logging
import sys

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from src.settings_window import SettingsWindow
from src.new_project_dialog import NewProjectDialog
from src.connection_manager_factory import ConnectionManagerFactory
from src.localizer import Localizer, LocaleNotFoundError, LocalizationKeyError

logger = logging.getLogger(__name__)


class ConnectionApp(tk.Tk):
    def __init__(self, language="en"):
        super().__init__()
        self.localizer = Localizer(language)
        self.title(self.localizer.get("application_title"))

        # Set the default window size
        self.geometry("800x600")

        # Call NewProjectDialog and wait until it's done
        self.new_project_dialog = NewProjectDialog(self, language=language)
        self.wait_window(self.new_project_dialog)
        self.new_project_result = self.new_project_dialog.result

        if self.new_project_result is None:
            self.quit()
            return

        # Get results from NewProjectDialog
        self.file_name = self.new_project_result.get("file_name")
        self.entry_mode = self.new_project_result.get("mode")
        self.file_path = self.new_project_result.get("file_path")

        self.connections_dict = {}
        self.tree_item_to_connection = {}
        self.selected_connections = []

        # Initialize the ConnectionManager
        if self.entry_mode and self.file_path:
            self.connection_manager = (
                ConnectionManagerFactory.create_connection_manager(
                    self.entry_mode, self.file_path
                )
            )
        else:
            messagebox.showerror(
                self.localizer.get("error"),
                self.localizer.get("error_connection_manager_init"),
            )
            sys.exit(0)

        self.lock_destination_toggle = tk.BooleanVar()

        # Sources
        self.source_increment_toggle = tk.BooleanVar()
        self.source_component = tk.StringVar()
        self.source_terminal_block = tk.StringVar()
        self.source_terminal = tk.StringVar()

        # Destinations
        self.destination_increment_toggle = tk.BooleanVar()
        self.destination_component = tk.StringVar()
        self.destination_terminal_block = tk.StringVar()
        self.destination_terminal = tk.StringVar()

        self.connection_frame = tk.Frame(self)
        self.create_widgets()
        self.load_connections()

    def create_widgets(self):
        # Define labels
        if self.file_name is None:
            self.file_name = self.localizer.get("untitled_labels")
        self.file_name_label = tk.Label(self, text=self.file_name)
        self.component_label = tk.Label(self, text=self.localizer.get("component"))
        self.terminal_block_label = tk.Label(
            self, text=self.localizer.get("terminal_block")
        )
        self.terminal_label = tk.Label(self, text=self.localizer.get("terminal"))
        self.file_name_field_label = tk.Label(
            self, text=self.localizer.get("saving_as").format(filename=self.file_name)
        )
        self.source_label = tk.Label(self, text=self.localizer.get("field_one"))
        self.destination_label = tk.Label(self, text=self.localizer.get("field_two"))
        self.status_label = tk.Label(self, text="")

        # Define Entry fields
        self.source_component_entry = tk.Entry(self, textvariable=self.source_component)
        self.source_terminal_block_entry = tk.Entry(
            self, textvariable=self.source_terminal_block
        )
        self.source_terminal_entry = tk.Entry(self, textvariable=self.source_terminal)

        self.destination_component_entry = tk.Entry(
            self, textvariable=self.destination_component
        )
        self.destination_terminal_block_entry = tk.Entry(
            self, textvariable=self.destination_terminal_block
        )
        self.destination_terminal_entry = tk.Entry(
            self, textvariable=self.destination_terminal
        )

        # Define Checkbuttons
        self.source_increment_checkbutton = tk.Checkbutton(
            self,
            text=self.localizer.get("increment"),
            variable=self.source_increment_toggle,
        )
        self.destination_increment_checkbutton = tk.Checkbutton(
            self,
            text=self.localizer.get("increment"),
            variable=self.destination_increment_toggle,
        )
        self.lock_destination_checkbutton = tk.Checkbutton(
            self,
            text=self.localizer.get("lock_destination"),
            variable=self.lock_destination_toggle,
        )

        # Define buttons
        self.save_button = tk.Button(
            self, text=self.localizer.get("save_file"), command=self.save_file
        )
        self.add_connection_button = tk.Button(
            self, text=self.localizer.get("add_connection"), command=self.add_connection
        )
        self.settings_button = tk.Button(
            self, text=self.localizer.get("settings"), command=self.open_settings_window
        )
        self.delete_button = tk.Button(
            self,
            text=self.localizer.get("delete_connection"),
            command=self.delete_connection,
        )
        self.export_button = tk.Button(
            self, text=self.localizer.get("export"), command=self.export_to_csv
        )

        # Define bindings
        self.source_component_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.source_terminal_entry.bind("<Return>", lambda event: self.add_connection())
        self.destination_component_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )
        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.add_connection()
        )

        # Define text area for connection numbers
        self.tree_widget = self.create_tree_widget()

        # Arrange widgets in grid (left to right, top to bottom)
        self.tree_widget.grid(row=1, column=0, rowspan=6, padx=5, pady=5)
        self.file_name_field_label.grid(
            row=0, column=3, columnspan=5, sticky="w", padx=5, pady=5
        )
        self.lock_destination_checkbutton.grid(row=2, column=4, padx=5, pady=5)

        self.component_label.grid(row=3, column=2, padx=5, pady=5)
        self.terminal_block_label.grid(row=3, column=3, padx=5, pady=5)
        self.terminal_label.grid(row=3, column=4, padx=5, pady=5)

        self.source_label.grid(row=5, column=1, padx=5, pady=5)
        self.source_component_entry.grid(row=5, column=2, padx=5, pady=5)
        self.source_terminal_block_entry.grid(row=5, column=3, padx=5, pady=5)
        self.source_terminal_entry.grid(row=5, column=4, padx=5, pady=5)
        self.source_increment_checkbutton.grid(row=5, column=5, padx=5, pady=5)

        self.destination_label.grid(row=6, column=1, padx=5, pady=5)
        self.destination_component_entry.grid(row=6, column=2, padx=5, pady=5)
        self.destination_terminal_block_entry.grid(row=6, column=3, padx=5, pady=5)
        self.destination_terminal_entry.grid(row=6, column=4, padx=5, pady=5)
        self.destination_increment_checkbutton.grid(row=6, column=5, padx=5, pady=5)
        self.add_connection_button.grid(row=7, column=2, padx=5, pady=5)
        self.settings_button.grid(row=7, column=5, padx=5, pady=5)

        self.delete_button.grid(row=7, column=0, padx=5, pady=5)

        self.save_button.grid(row=8, column=0, padx=5, pady=5)
        self.export_button.grid(row=8, column=1, padx=5, pady=5)

        self.status_label.grid(
            row=9, column=0, columnspan=5, sticky="w", padx=5, pady=5
        )
        self.update_connection_list()

    def create_tree_widget(self):
        columns = ("Source", "Destination")
        tree = ttk.Treeview(self, columns=columns, show="headings")

        # Define headings
        tree.heading("Source", text=self.localizer.get("source"))
        tree.heading("Destination", text=self.localizer.get("destination"))

        tree.bind("<<TreeviewSelect>>", self.update_selected_connections)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree["yscrollcommand"] = scrollbar.set  # Link the scrollbar to the treeview

        return tree

    def update_selected_connections(self, event):
        logger.info(f"event = {event}")

        # Get currently selected items
        selected_items = self.tree_widget.selection()
        logger.info(f"selected_items: {selected_items}")

        # Clear the selected connections list
        self.selected_connections = []

        # Add all currently selected connections to the list
        for item in selected_items:
            connection = self.tree_item_to_connection.get(item)
            if connection:
                self.selected_connections.append(connection)
                logger.info(f"selected_connections: {self.selected_connections}")

        logger.info(f"self.selected_connections = {self.selected_connections}")

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)

    def validate_json_content(self, content):
        try:
            json.loads(content)
        except json.JSONDecodeError:
            return False
        return True

    def increment(self, input_box: tk.Entry):
        try:
            value = int(input_box.get())
            input_box.delete(0, tk.END)
            input_box.insert(0, str(value + 1))
        except ValueError:
            self.display_status(self.localizer.get("increment_error"))

    def is_empty_label(
        self,
        source_component,
        source_terminal_block,
        source_terminal,
        destination_component,
        destination_terminal_block,
        destination_terminal,
    ) -> bool:
        if (
            source_component == ""
            and source_terminal_block == ""
            and source_terminal == ""
            and destination_component == ""
            and destination_terminal_block == ""
            and destination_terminal == ""
        ):
            return True
        return False

    def add_connection(self):
        source_component = self.source_component.get()
        source_terminal_block = self.source_terminal_block.get()
        source_terminal = self.source_terminal.get()

        if self.lock_destination_toggle.get():
            # Set destination fields to match source fields
            self.destination_component.set(source_component)
            self.destination_terminal_block.set(source_terminal_block)
            self.destination_terminal.set(source_terminal)

        destination_component = self.destination_component.get()
        destination_terminal_block = self.destination_terminal_block.get()
        destination_terminal = self.destination_terminal.get()

        # Check if every field is empty
        if self.is_empty_label(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        ):
            return

        connection = self.connection_manager.add_connection(
            source_component,
            source_terminal_block,
            source_terminal,
            destination_component,
            destination_terminal_block,
            destination_terminal,
        )

        source, destination = self.connection_manager.get_connection_tuple(connection)

        # Add to tree widget and get unique identifier
        item = self.tree_widget.insert("", "end", values=(source, destination))

        # Add to the mapping dictionary
        self.tree_item_to_connection[item] = connection

        # Print a message to the UI
        self.display_status(self.localizer.get("added_connection"))

        # Update the listbox to reflect the new connection list
        self.update_connection_list()

        if self.source_increment_toggle.get():
            self.increment(self.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.increment(self.destination_terminal_entry)

    def delete_connection(self):
        logger.info("delete")
        for item in self.tree_widget.selection():
            try:
                connection = self.tree_item_to_connection[item]
            except KeyError:
                logger.warning(f"Connection not found for item: {item}")
                continue
            logger.info(f"Deleting connection: {connection}")

            # Attempt to delete the connection
            try:
                self.connection_manager.delete_connection(connection)
            except Exception as e:
                logger.warning(
                    f"Could not delete {connection} from connection manager: {e}"
                )
                continue  # Skip this connection

            # Attempt to delete from connections_dict
            try:
                del self.connections_dict[str(connection)]
            except KeyError:
                logger.warning(f"Connection {connection} not found in connections_dict")

            # Attempt to delete from tree_item_to_connection
            try:
                del self.tree_item_to_connection[item]
            except KeyError:
                logger.warning(f"Item {item} not found in tree_item_to_connection")

        self.update_connection_list()
        self.selected_connections = []

    def populate_connections(self):
        self.connection_manager.load_from_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.tree_widget.insert("", "end", values=(source, destination))

    def update_connection_list(self):
        self.tree_widget.delete(
            *self.tree_widget.get_children()
        )  # clear the tree widget

        for connection in self.connection_manager.connections:
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            # Add to the tree widget and get unique identifier
            item_id = self.tree_widget.insert("", "end", values=(source, destination))

            # Add to the dictionaries
            self.connections_dict[str(connection)] = connection
            self.tree_item_to_connection[item_id] = connection

    def run_program(self):
        try:
            if self.file_path is None:
                self.file_path = "untitled"
            if self.entry_mode is None:
                self.entry_mode = "connection"
            self.connection_manager = (
                ConnectionManagerFactory.create_connection_manager(
                    self.entry_mode, self.file_path
                )
            )
        except ValueError as e:
            logger.info(f"Error: {e}")
            sys.exit(1)  # or however you want to handle this case

    def save_file(self) -> None:
        success = self.connection_manager.save_to_file()

        if success:
            self.display_status(self.localizer.get("success_file_added"))
        else:
            self.display_status(self.localizer.get("error_file_added"))

    def load_connections(self):
        self.connection_manager.load_from_file()
        self.update_connection_list()

    def export_to_csv(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if filename:  # if a filename was entered in the dialog
            try:
                self.connection_manager.export_to_csv(filename)
                self.display_status(self.localizer.get("exported_file"))
            except FileExistsError as e:
                self.display_status(str(e))

    def display_status(self, message) -> None:
        # Update the status label with the message
        self.status_label["text"] = message

        # Clear the status label after 5 seconds
        self.after(5000, lambda: self.status_label.config(text=""))
