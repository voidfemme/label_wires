import tkinter as tk
import logging
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext
from typing import TYPE_CHECKING
from src.ui.localized_widgets import LocalizedButton

from src.ui.settings_window import SettingsWindow
from src.ui.header import Header
from src.ui.tree_widget_frame import TreeWidgetFrame
from src.ui.connection_entry_frame import ConnectionEntryFrame
from src.ui.utility_buttons import UtilityButtonsFrame
from src.ui.footer import Footer

if TYPE_CHECKING:
    from src.localizer import Localizer


logger = logging.getLogger(__name__)

"""
Main View in the MVC (Model-View-Controller) pattern. This module instantiates and
manages the various frames that make up its contents.
"""


class MainView(tk.Tk):
    def __init__(
        self,
        controller,
        settings,
    ) -> None:
        super().__init__()
        self.controller = controller
        self.title(self.controller.localizer.get("application_title"))
        self.settings = settings
        self.geometry("1200x400")
        self.is_destroying = False
        self.create_widgets()
        self.arrange_widgets_in_grid()
        self.tree_widget.update_connection_list()

    def create_widgets(self) -> None:
        # Define labels
        self.header = Header(
            self,
            self.controller,
        )

        # Define text area for connection numbers
        self.entry_frame = ConnectionEntryFrame(
            self,
            self.controller,
        )
        self.tree_widget = TreeWidgetFrame(
            self,
            self.entry_frame,
            self.controller,
            self.controller.event_system,
        )

        self.utility_buttons_horizontal_rule = ttk.Separator(self, orient="horizontal")

        self.utility_buttons_frame = UtilityButtonsFrame(
            self, self.controller, self.controller.localizer
        )

        self.horizontal_rule_footer = ttk.Separator(self, orient="horizontal")
        self.footer = Footer(self, self.controller)

    def arrange_widgets_in_grid(self) -> None:
        # Arrange widgets in grid (left to right, top to bottom)
        self.header.grid(row=0, column=0, sticky="ew")
        self.tree_widget.grid(row=1, column=0, rowspan=6, padx=5, pady=5)
        self.entry_frame.grid(row=1, column=1, padx=5, pady=5)
        self.utility_buttons_horizontal_rule.grid(
            row=3, column=1, columnspan=5, sticky="ew", pady=5
        )
        self.utility_buttons_frame.grid(row=4, column=1, padx=5, pady=5)
        self.horizontal_rule_footer.grid(
            row=5, column=1, columnspan=5, sticky="ew", pady=5
        )
        self.footer.grid(row=6, column=1, sticky="ew")

    def scroll_to_bottom_of_treewidget(self) -> None:
        self.tree_widget.tree_widget.update_idletasks()
        self.tree_widget.tree_widget.yview_moveto(1)

    def save_file(self):
        file_name = self.controller.file_name
        if self.controller.save_to_json_file():
            self.display_status(
                self.controller.localizer.get("success_file_added").format(file_name)
            )
        else:
            self.display_status(self.controller.localizer.get("error_file_added"))

    def display_status(self, message) -> None:
        try:
            # Update the status label with the message
            self.footer.display_status(message)
        except tk.TclError:
            logger.critical("Status label does not exist.")

    def open_settings_window(self) -> None:
        self.settings_window = SettingsWindow(self, self.settings)

    def show_csv_preview(self, csv_data: str, localizer: "Localizer") -> bool:
        # Variable to store the user's decision (Export or Cancel)
        user_decision = tk.BooleanVar(value=False)

        # Create a new top-level window for the CSV preview
        preview_window = tk.Toplevel(self)
        preview_window.title("CSV Preview")
        preview_window.geometry("600x400")

        # Display the CSV data using a scrolled text widget
        text_widget = scrolledtext.ScrolledText(
            preview_window, wrap=tk.WORD, width=70, height=20
        )
        text_widget.pack(pady=20, padx=20)
        text_widget.insert(tk.END, csv_data)
        text_widget.configure(state=tk.DISABLED)  # Make the widget read-only

        # Function to handle the Export button click
        def on_export():
            user_decision.set(True)
            logger.info("MainView.show_csv_preview.on_export called")
            preview_window.destroy()

        # Function to handle the Cancel button click
        def on_cancel():
            user_decision.set(False)
            logger.info("MainView.show_csv_preview.on_cancel called")
            preview_window.destroy()

        export_button = LocalizedButton(preview_window, localizer, "export", command=on_export)
        export_button.pack(side=tk.LEFT, padx=10, pady=10)

        cancel_button = LocalizedButton(preview_window, localizer, "cancel", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Make the window modal (block interaction with other windows until this one is closed)
        preview_window.transient(self)
        preview_window.grab_set()
        self.wait_window(preview_window)

        return user_decision.get()

    def export_to_csv(self) -> None:
        self.controller.export_to_csv()

    def display_file_browser(self, *args, **kwargs):
        return filedialog.asksaveasfilename(*args, **kwargs)

    def prompt_save(self) -> bool:
        return messagebox.askyesno(
            title=self.controller.localizer.get("unsaved_changes"),
            message=self.controller.localizer.get("save_changes_prompt"),
        )

    def open_save_dialog(self) -> str:
        file_path = filedialog.asksaveasfilename(
            title=self.controller.localizer.get("save_file"),
            filetypes=[
                ("JSON files", "*.json"),
                ("Wire files", "*.wir"),
                ("All files", "*.*"),
            ],
            defaultextension=".wir",
        )
        return file_path

    def quit_program(self, quit_from_dialog: bool = False) -> None:
        self.is_destroying = True
        self.controller.handle_quit(quit_from_dialog)
        if quit_from_dialog is False:
            self.destroy()
