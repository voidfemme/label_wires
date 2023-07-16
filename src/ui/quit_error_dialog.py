import tkinter as tk
from tkinter import filedialog
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.controllers.controller import Controller


class QuitErrorDialog:
    def __init__(self, parent, controller: "Controller"):
        top = self.top = tk.Toplevel(parent)
        self.controller = controller
        tk.Label(top, text="An error occurred!").pack()

        tk.Button(top, text="Cancel", command=self.cancel).pack()
        tk.Button(
            top, text="Quit without saving", command=self.quit_without_saving
        ).pack()
        tk.Button(top, text="Save As", command=self.save).pack()

    def cancel(self):
        print("Cancel")
        self.top.destroy()

    def quit_without_saving(self):
        print("Quit ")
        self.controller.quit_program()

    def save(self):
        print("Save")
        file_path = filedialog.asksaveasfilename(title="Save Wire File as...")
        self.controller.set_file_path(file_path)
        self.top.destroy()
