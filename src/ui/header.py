import tkinter as tk


class Header(tk.Frame):
    def __init__(self, parent, localizer, settings, file_name):
        super().__init__(parent)
        self.parent = parent
        self.localizer = localizer
        self.settings = settings
        if file_name is None:
            self.file_name = self.localizer.get("untitled_labels")
        else:
            self.file_name = file_name
        self.file_name_label = tk.Label(self, text=self.file_name)
        self.file_name_label.grid(row=0, column=0)
