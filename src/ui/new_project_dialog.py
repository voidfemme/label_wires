import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
from typing import Any, Optional
import webbrowser
from src.localizer import Localizer
from src.settings import Settings
from src.ui.settings_window import SettingsWindow
from src.ui.localized_widgets import LocalizedLabel, LocalizedButton

"""
This is the dialog that pops up when the user opens the application.
It allows them to access settings, create a new project, or open an existing project.
"""


class NewProjectDialog(tk.Toplevel):
    def __init__(self, settings, localizer, parent: Optional[Any] = None) -> None:
        super().__init__(master=parent)
        self.settings = settings
        self.parent = parent
        self.localizer = localizer
        self.title("New Project")

        # Initialize all the variables
        self.file_base_name = tk.StringVar()
        self.directory = tk.StringVar()
        self.open_existing_file_directory = tk.StringVar()
        self.file_ext = {"wire": ".wir"}

        # Initialize result attribute
        self.result = None

        # Call method to create widgets
        self.create_widgets()

    def create_widgets(self) -> None:
        # Call methods to create specific sections of the GUI
        self.create_header_section()
        self.create_new_file_section()
        self.create_open_existing_file_section()
        self.create_csv_delimiter_section()
        self.create_info_section()

    def create_csv_delimiter_section(self) -> None:
        self.custom_csv_delimiter_label = LocalizedButton(
            self, self.localizer, "default_csv_delimiter"
        )

    def create_header_section(self) -> None:
        # Section belongs at the top left
        title_label = LocalizedLabel(self, self.localizer, "application_title")
        self.grid_columnconfigure(0, weight=1)
        title_label.grid(row=0, column=0, sticky="ew")

    def create_new_file_section(self) -> None:
        # Section belongs in the top left
        # Define the elements
        self.file_name_field_label = LocalizedLabel(
            self, self.localizer, "file_name_entry"
        )
        self.save_directory_label = LocalizedLabel(
            self, self.localizer, "save_in_directory"
        )

        self.file_name_field_entry = tk.Entry(self, textvariable=self.file_base_name)
        self.save_directory_entry = tk.Entry(self, textvariable=self.directory)

        self.browse_directory_button = LocalizedButton(
            self, self.localizer, "browse", command=self.browse_directory
        )
        self.create_button = LocalizedButton(
            self,
            self.localizer,
            "create_button",
            command=self.validate_and_create,
            state="disabled",
        )  # Add the widgets to the grid
        self.file_name_field_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.file_name_field_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.save_directory_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.save_directory_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
        self.browse_directory_button.grid(row=2, column=2, padx=10, pady=10)
        self.create_button.grid(row=2, column=3, padx=10, pady=10)
        self.grid_columnconfigure(1, weight=1)

        # Trace the tkinter variables
        self.file_base_name.trace("w", self.check_create_file_entry_fields)
        self.directory.trace("w", self.check_create_file_entry_fields)

    def create_open_existing_file_section(self) -> None:
        # Section in the bottom left
        # Define the elements
        self.open_existing_file_directory.trace("w", self.check_open_file_entry_fields)
        self.horizontal_rule = ttk.Separator(self, orient="horizontal")
        self.open_existing_file_label = LocalizedLabel(
            self, self.localizer, "open_existing_file_label"
        )
        self.open_existing_file_entry = tk.Entry(
            self, textvariable=self.open_existing_file_directory
        )
        self.browse_for_existing_files_button = LocalizedButton(
            self, self.localizer, "browse", command=self.open_file_browse
        )
        self.open_existing_file_button = LocalizedButton(
            self,
            self.localizer,
            "open_button",
            command=self.open_existing_file,
            state="disabled",
        )

        # Add the widgets to the grid
        self.open_existing_file_label.grid(
            row=5, column=0, sticky="w", padx=10, pady=10
        )
        self.open_existing_file_entry.grid(
            row=5, column=1, sticky="ew", padx=10, pady=10
        )
        self.browse_for_existing_files_button.grid(row=5, column=2, padx=10, pady=10)
        self.open_existing_file_button.grid(row=5, column=3, padx=10, pady=10)
        self.horizontal_rule.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)

    def create_info_section(self) -> None:
        # For settings and "about this app" information
        # Define the elements
        self.vertical_rule = ttk.Separator(self, orient="vertical")
        self.quit_button = LocalizedButton(
            self, self.localizer, "quit", command=self.quit_program
        )
        self.settings_button = LocalizedButton(
            self, self.localizer, "settings", command=self.open_settings
        )
        self.about_button = LocalizedButton(
            self, self.localizer, "about", command=self.open_about_popup
        )

        # Add the widgets to the grid
        self.vertical_rule.grid(row=0, column=4, rowspan=9, sticky="ns", padx=10)
        self.quit_button.grid(row=5, column=5, sticky="w", padx=10, pady=10)
        self.settings_button.grid(row=4, column=5, sticky="w", padx=10, pady=10)
        self.about_button.grid(row=3, column=5, sticky="w", padx=10, pady=10)

    def open_file_browse(self) -> None:
        filetypes = (
            ("wire files", "*.wir"),
            ("all files", "*.*"),
        )
        filepath = filedialog.askopenfilename(
            title=self.localizer.get("open_file"), filetypes=filetypes
        )

        if filepath:  # If the user didn't cancel the dialog
            self.open_existing_file_directory.set(filepath)

    def browse_directory(self) -> None:
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)

    def check_open_file_entry_fields(self, *args) -> None:
        if self.open_existing_file_directory.get():
            self.open_existing_file_button["state"] = "normal"
        else:
            self.open_existing_file_button["state"] = "disabled"

    def check_create_file_entry_fields(self, *args) -> None:
        if self.file_base_name.get() and self.directory.get():
            self.create_button["state"] = "normal"
        else:
            self.create_button["state"] = "disabled"

    def validate_and_create(self) -> None:
        directory = Path(self.directory.get())
        file_name = self.file_base_name.get()
        file_path = directory / file_name

        if file_path.exists():
            messagebox.showerror(
                self.localizer.get("file_exists"),
                self.localizer.get("file_already_exists"),
            )
        else:
            self.apply()

    def open_existing_file(self) -> None:
        file_path = Path(self.open_existing_file_directory.get())

        if not file_path.exists():
            messagebox.showerror(
                self.localizer.get("file_not_found"),
                self.localizer.get("file_not_found_message"),
            )
        else:
            file_name = file_path.name
            self.result = {
                "file_path": str(file_path),
                "file_name": file_name,
            }
            self.destroy()

    def open_settings(self) -> None:
        self.settings_window = SettingsWindow(self, self.settings)

    def open_url(self, url) -> None:
        webbrowser.open_new(url)

    def open_about_popup(self) -> None:
        about_win = tk.Toplevel(self)
        about_win.title(self.localizer.get("about"))
        about_text = (
            self.localizer.get("application_title")
            + "\n"
            + self.localizer.get("created_by_rose")
            + "\n"
            + self.localizer.get("love_is_love")
            + "\n"
            + self.localizer.get("bugs_issues_message")
        )
        link = "https://github.com/voidfemme/label_wires"
        label1 = tk.Label(about_win, text=about_text, justify=tk.LEFT)
        label1.pack(side="top")
        label2 = tk.Label(about_win, text=link, fg="blue", cursor="hand2")
        label2.pack(side="top")
        label2.bind("<Button-1>", lambda e: self.open_url(link))

    def quit_program(self) -> None:
        self.parent.quit_program()  # type: ignore

    def apply(self) -> None:
        directory = Path(self.directory.get())
        file_name = self.file_base_name.get()

        file_path = directory / (file_name + ".wir")

        if file_path.exists():
            messagebox.showerror(
                self.localizer.get("file_exists"),
                self.localizer.get("file_exists_message"),
            )
        else:
            # Create the new project file
            try:
                with open(file_path, "w") as f:
                    pass

                self.result = {
                    "file_path": str(file_path),
                    "file_name": file_name,
                }
            except Exception as e:
                messagebox.showerror(self.localizer.get("error"), str(e))
        self.destroy()
