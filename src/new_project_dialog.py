#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import webbrowser
from src.localizer import Localizer
from src.settings import Settings
from src.settings_window import SettingsWindow


class NewProjectDialog(tk.Toplevel):
    def __init__(self, master=None, language="en"):
        super().__init__(master=master)
        self.master = master
        self.language = language
        self.localizer = Localizer(self.language)
        self.title("New Project")

        # Initialize all the variables
        self.file_base_name = tk.StringVar()
        self.directory = tk.StringVar()
        self.file_mode = tk.StringVar()
        self.open_existing_file_directory = tk.StringVar()
        self.file_ext = {"cable": ".cab", "wire": ".wir"}

        # Initialize result attribute
        self.result = None

        # Call method to create widgets
        self.create_widgets()

    def create_widgets(self):
        # Call methods to create specific sections of the GUI
        self.create_header_section()
        self.create_new_file_section()
        self.create_open_existing_file_section()
        self.create_csv_delimiter_section()
        self.create_info_section()

    def create_csv_delimiter_section(self):
        self.custom_csv_delimiter_label = tk.Label(
            self, text=self.localizer.get("default_csv_delimiter")
        )

    def create_header_section(self):
        # Section belongs at the top left
        title_label = tk.Label(self, text=self.localizer.get("application_title"))
        self.grid_columnconfigure(0, weight=1)
        title_label.grid(row=0, column=0, sticky="ew")

    def create_new_file_section(self):
        # Section belongs in the top left
        # Define the elements
        self.file_name_field_label = tk.Label(
            self, text=self.localizer.get("file_name_entry")
        )
        self.save_directory_label = tk.Label(
            self, text=self.localizer.get("save_in_directory")
        )
        self.entry_mode_label = tk.Label(self, text=self.localizer.get("entry_mode"))

        self.file_name_field_entry = tk.Entry(self, textvariable=self.file_base_name)
        self.save_directory_entry = tk.Entry(self, textvariable=self.directory)
        self.entry_mode_entry = ttk.Combobox(
            self, textvariable=self.file_mode, values=("cable", "wire")
        )

        self.browse_directory_button = tk.Button(
            self,
            text=self.localizer.get("browse"),
            command=self.browse_directory,
        )
        self.create_button = tk.Button(
            self,
            text=self.localizer.get("create_button"),
            command=self.validate_and_create,
        )

        # Add the widgets to the grid
        self.file_name_field_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.file_name_field_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.save_directory_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.save_directory_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
        self.entry_mode_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.entry_mode_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)
        self.browse_directory_button.grid(row=2, column=2, padx=10, pady=10)
        self.create_button.grid(row=2, column=3, padx=10, pady=10)
        self.grid_columnconfigure(1, weight=1)

        # Trace the tkinter variables
        self.file_base_name.trace("w", self.check_fields)
        self.directory.trace("w", self.check_fields)
        self.file_mode.trace("w", self.check_fields)

    def create_open_existing_file_section(self):
        # Section in the bottom left
        # Define the elements
        self.horizontal_rule = ttk.Separator(self, orient="horizontal")
        self.open_existing_file_label = tk.Label(
            self, text=self.localizer.get("open_existing_file_label")
        )
        self.open_existing_file_entry = tk.Entry(
            self, textvariable=self.open_existing_file_directory
        )
        self.browse_for_existing_files_button = tk.Button(
            self,
            text=self.localizer.get("browse"),
            command=self.open_file_browse,
        )
        self.open_existing_file_button = tk.Button(
            self,
            text=self.localizer.get("open_button"),
            command=self.open_existing_file,
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

    def create_info_section(self):
        # For settings and "about this app" information
        # Define the elements
        self.vertical_rule = ttk.Separator(self, orient="vertical")
        self.quit_button = tk.Button(
            self, text=self.localizer.get("quit"), command=self.quit_program
        )
        self.settings_button = tk.Button(
            self, text=self.localizer.get("settings"), command=self.open_settings
        )
        self.about_button = tk.Button(
            self, text=self.localizer.get("about"), command=self.open_about_popup
        )

        # Add the widgets to the grid
        self.vertical_rule.grid(row=0, column=4, rowspan=9, sticky="ns", padx=10)
        self.quit_button.grid(row=5, column=5, sticky="w", padx=10, pady=10)
        self.settings_button.grid(row=4, column=5, sticky="w", padx=10, pady=10)
        self.about_button.grid(row=3, column=5, sticky="w", padx=10, pady=10)

    def open_file_browse(self):
        filetypes = (
            ("cable files", "*.cab"),
            ("wire files", "*.wir"),
            ("all files", "*.*"),
        )
        filepath = filedialog.askopenfilename(
            title=self.localizer.get("open_file"), filetypes=filetypes
        )

        if filepath:  # If the user didn't cancel the dialog
            self.open_existing_file_directory.set(filepath)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)

    def check_fields(self, *args):
        if self.file_base_name.get() and self.directory.get() and self.file_mode.get():
            self.create_button["state"] = "normal"
        else:
            self.create_button["state"] = "disabled"

    def validate_and_create(self):
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

    def open_existing_file(self):
        file_path = Path(self.open_existing_file_directory.get())

        if not file_path.exists():
            messagebox.showerror(
                self.localizer.get("file_not_found"),
                self.localizer.get("file_not_found_message"),
            )
        else:
            file_name = file_path.name
            mode = "wire" if str(file_path).endswith(".wir") else "cable"
            # If the file does not exist, store its path as the result and close the dialog
            self.result = {
                "file_path": str(file_path),
                "file_name": file_name,
                "mode": mode,
            }
            self.destroy()

    def open_settings(self):
        self.settings = Settings()
        self.settings_window = SettingsWindow(
            self, self.settings, language=self.language
        )

    def open_url(self, url):
        webbrowser.open_new(url)

    def open_about_popup(self):
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

    def quit_program(self):
        self.master.quit_program()

    def apply(self):
        directory = Path(self.directory.get())
        file_name = self.file_base_name.get()
        mode = self.file_mode.get()

        if mode == "wire":
            file_ext = ".wir"
        elif mode == "cable":
            file_ext = ".cab"
        else:
            file_ext = ".json"
        file_path = directory / (file_name + file_ext)

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
                    "mode": mode,
                }
            except Exception as e:
                messagebox.showerror(self.localizer.get("error"), str(e))
        self.destroy()
