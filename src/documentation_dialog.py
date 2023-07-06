import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import webbrowser

from src.localizer import Localizer
from src.localized_widgets import LocalizedTreeview, LocalizedButton

"""
This is the documentation dialog box. It displays a treewidget and a text area that has
information about how to use the project.
"""


class DocumentationDialog(tk.Toplevel):
    def __init__(self, master=None) -> None:
        self.master = master
        self.localizer = Localizer("en")
        self.title("WireLab Documentation")

        self.create_document_selector()
        self.create_document_reader()

        self.close_button = LocalizedButton(self, self.localizer, l10n_key="close")
        self.layout_elements()

    def create_document_selector(self):
        columns = "#1"
        columns_keys = ["topic"]
        self.columns_keys_mapping = dict(zip(columns, columns_keys))

    def create_document_reader(self):
        pass

    def layout_elements(self):
        pass
