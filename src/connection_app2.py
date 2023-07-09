# Love is love. Be yourself!
import logging
import tkinter as tk
import sys
import json

from tkinter import ttk, messagebox, filedialog

from src.command import AddConnectionCommand, DeleteConnectionCommand, EditConnectionCommand
from src.settings import Settings
from src.settings_window import SettingsWindow
from src.new_project_dialog import NewProjectDialog
from src.connection_manager_factory import ConnectionManagerFactory
from src.localizer import Localizer
from src.localized_widgets import (
    LocalizedLabel,
    LocalizedButton,
    LocalizedCheckButton,
    LocalizedTreeview,
)

logger = logging.getLogger(__name__)


class Header(tk.Frame):
    def __init__(self, parent, main_app, header_text, **kwargs):
        # super().__init__(parent, **kwargs)
        self.main_app = main_app
        self.header_text = header_text
        if self.main_app.file_name is None:
            self.main_app.set_file_name(self.header_text)
        self.file_name_label = tk.Label(self, text=self.main_app.file_name)


class WireListFrame(tk.Frame):
    def __init__(self, parent, main_app, settings, selected_connections, **kwargs):
        # super().__init__(parent, **kwargs)
        self.settings = settings
        self.localizer = Localizer(self.settings.get("language"))
        self.main_app = main_app
        self.selected_connections = selected_connections

        # Create the tree widget
        self.tree_widget = self.create_tree_widget()

        # Create a button frame and place it below the treewidget
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0)

        # Populate the button frame with buttons
        self.edit_button = LocalizedButton(
            self.button_frame, self.localizer, "edit", command=self.main_app.save_file
        )
        self.edit_button.grid(row=0, column=0)

        self.delete_button = LocalizedButton(
            self.button_frame,
            self.localizer,
            "delete_connection",
            command=self.main_app.delete_connection,
        )
        self.delete_button.grid(row=0, column=1)

    def create_tree_widget(self) -> LocalizedTreeview:
        columns = ("#1", "#2")
        columns_keys = ["source", "destination"]
        self.columns_keys_mapping = dict(zip(columns, columns_keys))
        tree = LocalizedTreeview(
            self, self.localizer, self.columns_keys_mapping, show="headings"
        )

        tree.bind("<<TreeviewSelect>>", self.main_app.update_selected_connections)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree["yscrollcommand"] = scrollbar.set  # Link the scrollbar to the treeview

        return tree

    def update_selected_connections(self, event) -> None:
        logger.info(f"event = {event}")

        # Get currently selected items
        selected_items = self.tree_widget.selection()
        logger.info(f"selected_items: {selected_items}")

        # Clear the selected connections list
        self.selected_connections = []

        # Add all currently selected connections to the list
        for item in selected_items:
            connection = self.main_app.tree_item_to_connection.get(item)
            if connection:
                self.selected_connections.append(connection)


class EntrySection(tk.Frame):
    def __init__(self, parent, main_app, settings, **kwargs):
        # super().__init__(parent, **kwargs)
        self.settings = settings
        self.localizer = Localizer(self.settings.get("language"))
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        # Define source widgets
        # Define all these together so that they snap together in a grid evenly.
        self.component_label = LocalizedLabel(self, self.localizer, "component")
        self.component_label.grid(row=0, column=1, padx=10, pady=10)

        self.terminal_block_label = LocalizedLabel(
            self, self.localizer, "terminal_block"
        )
        self.terminal_block_label.grid(row=0, column=2, padx=10, pady=10)

        self.terminal_label = LocalizedLabel(self, self.localizer, "terminal")
        self.terminal_label.grid(row=0, column=3, padx=10, pady=10)

        # Source Entry Fields
        self.field_one_label = LocalizedLabel(self, self.localizer, "field_one")
        self.field_one_label.grid(row=1, column=0, padx=10, pady=10)

        self.source_component_entry = tk.Entry(
            self, textvariable=self.main_app.source_component
        )
        self.source_component_entry.grid(row=1, column=2, padx=10, pady=10)

        self.source_terminal_block_entry = tk.Entry(
            self, textvariable=self.main_app.source_terminal_block
        )
        self.source_terminal_block_entry.grid(row=1, column=3, padx=10, pady=10)

        self.source_terminal_entry = tk.Entry(
            self, textvariable=self.main_app.source_terminal
        )
        self.source_terminal_entry.grid(row=1, column=4, padx=10, pady=10)

        self.source_increment_toggle = LocalizedCheckButton(
            self,
            self.localizer,
            "increment",
            variable=self.main_app.destination_increment_toggle,
        )
        self.source_increment_toggle.grid(row=1, column=5, padx=10, pady=10)

        # Destination Entry Fields
        self.field_two_label = LocalizedLabel(self, self.localizer, "field_two")
        self.field_two_label.grid(row=2, column=0, padx=10, pady=10)

        self.destination_component_entry = tk.Entry(
            self, textvariable=self.main_app.destination_component
        )
        self.destination_component_entry.grid(row=2, column=2, padx=10, pady=10)

        self.destination_terminal_block_entry = tk.Entry(
            self, textvariable=self.main_app.destination_terminal_block
        )
        self.destination_terminal_block_entry.grid(row=2, column=3, padx=10, pady=10)

        self.destination_terminal_entry = tk.Entry(
            self, textvariable=self.main_app.destination_terminal
        )
        self.destination_terminal_entry.grid(row=2, column=4, padx=10, pady=10)

        self.destination_increment_toggle = LocalizedCheckButton(
            self,
            self.localizer,
            "increment",
            variable=self.main_app.destination_increment_toggle,
        )
        self.destination_increment_toggle.grid(row=2, column=5, padx=10, pady=10)

        # Undo and Add Buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=3, column=3, sticky="E")

        self.undo_button = LocalizedButton(
            self.button_frame, self.localizer, "undo", command=self.main_app.undo
        )
        self.undo_button.grid(row=0, column=0)
        self.add_button = LocalizedButton(
            self.button_frame,
            self.localizer,
            "add_connection",
            command=self.main_app.add_connection,
        )
        self.add_button.grid(row=0, column=1)

    def define_keybindings(self) -> None:
        self.source_component_entry.bind(
            "<Return>", lambda event: self.main_app.add_connection()
        )

        self.source_terminal_block_entry.bind(
            "<Return>", lambda event: self.main_app.add_connection()
        )

        self.source_terminal_entry.bind(
            "<Return>", lambda event: self.main_app.add_connection()
        )

        self.destination_component_entry.bind(
            "<Return>", lambda event: self.main_app.add_connection()
        )

        self.destination_terminal_block_entry.bind(
            "<Return>", lambda event: self.main_app.add_connection()
        )

        self.destination_terminal_entry.bind(
            "<Return>", lambda event: self.main_app.add_connection()
        )


class UtilityButtons(tk.Frame):
    def __init__(self, parent, main_app, settings, **kwargs):
        # super().__init__(parent, **kwargs)
        self.settings = settings
        self.localizer = Localizer(self.settings.get("language"))
        self.main_app = main_app

        # Define buttons and place in grid
        self.save_button = LocalizedButton(
            self, self.localizer, "save_file", command=self.main_app.save_file
        )
        self.save_button.grid(row=0, column=0)
        self.export_button = LocalizedButton(
            self, self.localizer, "export", command=self.main_app.export_to_csv
        )
        self.export_button.grid(row=0, column=1)
        self.settings_button = LocalizedButton(
            self, self.localizer, "settings", command=self.main_app.open_settings_window
        )
        self.settings_button.grid(row=0, column=2)
        self.quit_button = LocalizedButton(
            self, self.localizer, "quit", command=self.main_app.quit_program
        )
        self.quit_button.grid(row=0, column=3)


class Footer(tk.Frame):
    def __init__(self, parent, main_app, settings, **kwargs):
        # super().__init__(parent, **kwargs)
        self.settings = settings
        self.localizer = Localizer(self.settings.get("language"))
        self.main_app = main_app

        self.number_of_connections = tk.Label(self, text="")
        self.status_label = tk.Label(self, text="")
        self.status_label.grid(row=0, column=0)


class MainApp(tk.Tk):
    def __init__(self) -> None:
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("language"))
        self.title("hello world")
        self.undo_stack = []  # Stack for actions for undo

        self.geometry("1300x400")  # Set the default window size

        self.withdraw()  # Hide the main window
        self.get_new_project_dialog_results()  # Show the opening dialog for setup

        self.connections_dict = {}  # for holding the list of connections in the UI?
        self.tree_item_to_connection = {}  # What is this for?
        self.selected_connections = []  # user-selected connections

        self.initialize_connection_manager()
        self.initialize_variables()
        self.create_frames()
        self.deiconify()

    def get_new_project_dialog_results(self) -> None:
        self.new_project_dialog = NewProjectDialog(self)
        self.wait_window(self.new_project_dialog)
        self.new_project_result = self.new_project_dialog.result
        if self.new_project_result is None:
            # Handle this case with an error message
            self.quit()
            return

        self.file_name = self.new_project_result.get("file_name")
        self.entry_mode = self.new_project_result.get("mode")
        self.file_path = self.new_project_result.get("file_path")

    def initialize_connection_manager(self) -> None:
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

    def initialize_variables(self) -> None:
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

    def create_frames(self) -> None:
        # Create and place frames on the grid just as you would with any other widget
        # Header
        self.header = Header(self, self, self.file_name)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Wire List
        self.wire_list_frame = WireListFrame(
            self, self, self.settings, self.selected_connections
        )
        self.wire_list_frame.grid(row=1, column=0, sticky="ns")

        # Main Entry Section
        self.entry_section = EntrySection(self, self, self.settings)

        # Utilities
        self.utility_buttons = UtilityButtons(self, self, self.settings)

        # Footer
        self.footer = Footer(self, self, self.settings)
        self.footer.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_selected_connections(self, event) -> None:
        logger.info(f"event = {event}")

        # Get currently selected items
        selected_items = self.wire_list_frame.tree_widget.selection()
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

    def open_settings_window(self) -> None:
        self.settings = Settings()
        self.settings_window = SettingsWindow(self, self.settings)

    def validate_json_content(self, content) -> bool:
        try:
            json.loads(content)
        except json.JSONDecodeError:
            return False
        return True

    def increment(self, input_box: tk.Entry) -> None:
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

    def add_connection(self) -> None:
        source = {
            "component": self.source_component.get(),
            "terminal_block": self.source_terminal_block.get(),
            "terminal": self.source_terminal.get(),
        }

        if self.lock_destination_toggle.get():
            # Set destination fields to match source fields
            self.destination_component.set(source["component"])
            self.destination_terminal_block.set(source["terminal_block"])
            self.destination_terminal.set(source["terminal"])

        destination = {
            "component": self.destination_component.get(),
            "terminal_block": self.destination_terminal_block.get(),
            "terminal": self.destination_terminal.get(),
        }

        # Check if every field is empty
        if self.is_empty_label(
            source["component"],
            source["terminal_block"],
            source["terminal"],
            destination["component"],
            destination["terminal_block"],
            destination["terminal"],
        ):
            return

        cmd = AddConnectionCommand(self, source, destination)
        cmd.execute()
        self.undo_stack.append(cmd)

        if self.source_increment_toggle.get():
            self.increment(self.entry_section.source_terminal_entry)
        if self.destination_increment_toggle.get():
            self.increment(self.entry_section.destination_terminal_entry)
        self.wire_list_frame.tree_widget.yview_moveto(1)

    def undo(self) -> None:
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()

    def delete_connection(self) -> None:
        command = DeleteConnectionCommand(self)
        command.execute()
        self.undo_stack.append(command)

        self.update_connection_list()
        self.selected_connections = []

    def edit_connection(self) -> None:
        # First, make sure only one item was selected.

        # Then, populate the fields with the item's values.

        # Use an EditConnectionCommand in order to be able to re-add the old connection
        # command = EditConnectionCommand(self)
        pass

    def populate_connections(self) -> None:
        self.connection_manager.load_json_from_file()
        for connection in self.connection_manager.get_connections():
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            self.wire_list_frame.tree_widget.insert(
                "", "end", values=(source, destination)
            )

    def update_connection_list(self) -> None:
        self.wire_list_frame.tree_widget.delete(
            *self.wire_list_frame.tree_widget.get_children()
        )  # clear the tree widget

        for connection in self.connection_manager.connections:
            source, destination = self.connection_manager.get_connection_tuple(
                connection
            )
            # Add to the tree widget and get unique identifier
            item_id = self.wire_list_frame.tree_widget.insert(
                "", "end", values=(source, destination)
            )

            # Add to the dictionaries
            self.connections_dict[str(connection)] = connection
            self.tree_item_to_connection[item_id] = connection

    def run_program(self) -> None:
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
        success = self.connection_manager.save_json_to_file()

        if success:
            self.display_status(
                self.localizer.get("success_file_added").format(self.file_path)
            )
        else:
            self.display_status(self.localizer.get("error_file_added"))

    def load_connections(self):
        self.connection_manager.load_json_from_file()
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
        self.footer.status_label["text"] = message

        # Clear the status label after 5 seconds
        self.after(5000, lambda: self.footer.status_label.config(text=""))

    def quit_program(self) -> None:
        self.destroy()
        sys.exit(0)
