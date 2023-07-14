import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path
import webbrowser

from src.localizer import Localizer
from src.ui.localized_widgets import LocalizedTreeview, LocalizedButton
from src.settings import Settings

"""
This is the documentation dialog box. It displays a treewidget and a text area that has
information about how to use the project.
"""


class DocumentationDialog(tk.Toplevel):
    def __init__(
        self,
        master=None,
        language="en",
    ) -> None:
        super().__init__(master=master)
        self.master = master  # type: ignore
        self.settings = Settings()
        self.localizer = Localizer(self.settings.get("settings"))
        self.title("WireLab Documentation")

        # Initialize variables
        self.doc_folder = Path("docs")
        self.result = None

        # Create widgets
        self.tree = ttk.Treeview(master, selectmode="browse")
        self.doc_text = scrolledtext.ScrolledText(master)

        # Place widgets
        self.tree.pack(side="left", fill="y")
        self.doc_text.pack(side="right", fill="both", expand=True)

        self.load_docs()

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_docs(self):
        for file_path in self.doc_folder.iterdir():
            self.tree.insert("", "end", text=file_path.name, values=[str(file_path)])

    def on_tree_select(self, event):
        item_id = self.tree.selection()[0]
        file_path = Path(self.tree.item(item_id)["values"][0])

        with file_path.open("r") as file:
            self.doc_text.delete("1.0", tk.END)
            self.doc_text.insert(tk.END, file.read())
